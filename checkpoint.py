
import openpmd_api as io
import numpy as np


class openpmdcopy:
    
    def __init__(self, input_path, output_path, iteration=0):
        
        self.read_series = io.Series(input_path, io.Access.read_only)
        self.write_series = io.Series(output_path, io.Access.create)
       
        self.input_iteration = self.read_series.iterations[iteration]
        self.output_iteration = self.write_series.iterations[iteration]
    
    def close(self):
        del self.read_series
        del self.write_series
        print('\ndata written and files closed')
        
    def copy(self, exclude_mesh=[]):
        input_particle_container = self.input_iteration.particles
        output_particle_container = self.output_iteration.particles

        self.__copy_particle_container(input_particle_container,
                                       output_particle_container)


        # copy/write field data
        input_mesh_container = self.input_iteration.meshes
        output_mesh_container = self.output_iteration.meshes

        self.__copy_mesh_container(input_mesh_container,
                                   output_mesh_container,
                                   exclude_mesh)
        
        self.close()
        
    def copy_series_data(self):
        self.copy_series_attributes(self.read_series, self.write_series)
        self.copy_attributes(self.input_iteration, self.output_iteration)

    def __copy_mesh_container(self,
                              input_mesh_container,
                              output_mesh_container,
                              exclude_mesh):
        
        self.copy_attributes(input_mesh_container, output_mesh_container)

        for mesh in input_mesh_container:
            if mesh in exclude_mesh:
                print("don't copy mesh:", mesh)
                continue
            print('mesh:', mesh)

            input_mesh = input_mesh_container[mesh]
            output_mesh = output_mesh_container[mesh]

            self.__copy_mesh(input_mesh, output_mesh)

            self.write_series.flush()


    def __copy_mesh(self, input_mesh, output_mesh):
        
        self.copy_attributes(input_mesh, output_mesh)

        for mesh_record_component in input_mesh:
            print('  mesh_record_component:', mesh_record_component)

            input_mesh_record_component = input_mesh[mesh_record_component]
            output_mesh_record_component = output_mesh[mesh_record_component]

            self.__copy_mesh_record_component(input_mesh_record_component,
                                              output_mesh_record_component)
            self.write_series.flush()


    def __copy_mesh_record_component(self,
                                     input_mesh_record_component,
                                     output_mesh_record_component):
        
        self.copy_attributes(input_mesh_record_component,
                             output_mesh_record_component)

        data_dtype = input_mesh_record_component.dtype
        data_shape = input_mesh_record_component.shape

        dataset = io.Dataset(data_dtype, data_shape)
        output_mesh_record_component.reset_dataset(dataset)

        data = input_mesh_record_component.load_chunk()
        self.read_series.flush()

        output_mesh_record_component.store_chunk(data)
        self.write_series.flush()
        
        del data



    #### write particle data ####

    def __copy_particle_container(self,
                                  input_particle_container,
                                  output_particle_container):
        
        self.copy_attributes(input_particle_container,
                             output_particle_container)

        for particle_species in input_particle_container:
            print('species:', particle_species)

            input_particle_species = input_particle_container[particle_species]
            output_particle_species = output_particle_container[particle_species]

            self.__copy_particle_species(input_particle_species,
                                         output_particle_species)

            input_particle_patches = input_particle_species.particle_patches
            output_particle_patches = output_particle_species.particle_patches

            self.__copy_particle_patches(input_particle_patches,
                                         output_particle_patches)


    def __copy_particle_species(self,
                                input_particle_species,
                                output_particle_species):
        
        self.copy_attributes(input_particle_species, output_particle_species)

        for record in input_particle_species:
            print('  record:', record)

            input_record = input_particle_species[record]
            output_record = output_particle_species[record]

            self.__copy_record(input_record, output_record, record)

            self.write_series.flush()


    def __copy_record(self, input_record, output_record, record):
        self.copy_attributes(input_record, output_record)

        for record_component in input_record:
            print('    record_component:', record_component)

            input_record_component = input_record[record_component]
            output_record_component = output_record[record_component]

            self.__copy_record_component(input_record_component,
                                         output_record_component)
            self.write_series.flush()


    def __copy_record_component(self,
                                input_record_component,
                                output_record_component):
        
        self.copy_attributes(input_record_component, output_record_component)

        is_constant = input_record_component.constant

        if is_constant:
            value = input_record_component.get_attribute('value')
            output_record_component.make_constant(value)

            return

        data_dtype = input_record_component.dtype
        data_shape = input_record_component.shape

        dataset = io.Dataset(data_dtype, data_shape)
        output_record_component.reset_dataset(dataset)

        data = input_record_component.load_chunk()
        self.read_series.flush()
        
        output_record_component.store_chunk(data)
        self.write_series.flush()



    #### write particle patch data ####

    def __copy_particle_patches(self,
                                input_particle_patches,
                                output_particle_patches):
        
        self.copy_attributes(input_particle_patches, output_particle_patches)

        for patch_record in input_particle_patches:
            print('  patch_record:', patch_record)

            input_patch_record = input_particle_patches[patch_record]
            output_patch_record = output_particle_patches[patch_record]

            self.__copy_patch_record(input_patch_record, output_patch_record)

        self.write_series.flush()


    def __copy_patch_record(self, input_patch_record, output_patch_record):
        self.copy_attributes(input_patch_record, output_patch_record)

        for patch_record_component in input_patch_record:
            print('    patch_record_component:', patch_record_component)

            input_patch_record_component = input_patch_record[patch_record_component]
            output_patch_record_component = output_patch_record[patch_record_component]

            self.__copy_patch_record_component(input_patch_record_component, output_patch_record_component)


    def __copy_patch_record_component(self,
                                      input_patch_record_component,
                                      output_patch_record_component):
        
        self.copy_attributes(input_patch_record_component,
                             output_patch_record_component)

        data_dtype = input_patch_record_component.dtype
        data_shape = input_patch_record_component.shape

        dataset = io.Dataset(data_dtype, data_shape)
        output_patch_record_component.reset_dataset(dataset)

        data = input_patch_record_component.load()
        self.read_series.flush()


        for i in range(np.prod(data_shape)):
            output_patch_record_component.store(i, data[i])
        
    
    def copy_attributes(self, inputAtr, outputAtr):
        force_attribute_list = ['shape', 'position', 'axisLabels',
                                'gridGlobalOffset', 'gridSpacing']
        dtypes = inputAtr.attribute_dtypes
        
        for attribute in inputAtr.attributes:
            attribute_value = inputAtr.get_attribute(attribute)
            
            if attribute in force_attribute_list:
                if type(attribute_value) != list:
                    attribute_value = [attribute_value]
                    
            outputAtr.set_attribute(attribute,
                                    attribute_value,
                                    dtypes[attribute])

    def copy_series_attributes(self, inputAtr, outputAtr):
        attributes_to_copy = ['author', 'basePath',
                              'iterationEncoding','iterationFormat',
                              'meshesPath', 'openPMDextension', 'openPMD',
                              'particlesPath']
        
        for attribute in inputAtr.attributes:
            if attribute in attributes_to_copy:
                continue
            attribute_value = inputAtr.get_attribute(attribute)
            outputAtr.set_attribute(attribute, attribute_value)
            
    def print_attributes(self, obj):
        print_attributes(obj)
            
            
            
def print_attributes(obj):
    try:
        dtypes = obj.attribute_dtypes
        
        for attribute in obj.attributes:
            print(attribute, ":", obj.get_attribute(attribute),
                  " - ", dtypes[attribute])
            
        print()
    except Exception as e:
        print('error in print attributes', e)
