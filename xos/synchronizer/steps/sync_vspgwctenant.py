# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import time
from django.db.models import Q, F
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

class SyncVSPGWCTenant(SyncInstanceUsingAnsible):
    observes = VSPGWCTenant
    template_name = "vspgwctenant_playbook.yaml"
    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncVSPGWCTenant, self).__init__(*args, **kwargs)

    def get_extra_attributes(self, o):

        scenario = self.get_scenario()

        if scenario == 'normal_scenario':
            return self.get_values_for_normal_scenario()
        elif scenario == 'normal_scenario_without_sdncontroller':
            return self.get_values_for_normal_scenario_wo_sdncontroller()
        elif scenario == 'emulator_scenario':
            return self.get_values_for_emulator_scenario()
        elif scenario == 'emulator_scenario_without_sdncontroller':
            return self.get_values_for_emulator_scenario_wo_sdncontroller()
        else:
            return self.get_extra_attributes_for_manual()

    # fields for manual case
    def get_extra_attributes_for_manual(self):
        fields = {}
        fields['scenario'] = self.get_scenario()
        # for interface.cfg file
        fields['zmq_sub_ip'] = "manual"
        fields['zmq_pub_ip'] = "manual"
        fields['dp_comm_ip'] = "manual"
        fields['cp_comm_ip'] = "manual"
        fields['fpc_ip'] = "manual"
        fields['cp_nb_server_ip'] = "manual"

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = "manual"
        fields['s11_mme_ip'] = "manual"
        fields['s1u_sgw_ip'] = "manual"

        # for rules setup in ONOS
        fields['sgi_as_ip'] = "manual"
        fields['sgi_spgwu_ip'] = "manual"

        return fields

    def get_values_for_normal_scenario(self):
        fields = {}
        fields['scenario'] = "normal_scenario"
        # for interface.cfg file
        fields['zmq_sub_ip'] = self.get_ip_address('sbi_network', SDNControllerServiceInstance, 'zmq_sub_ip')
        fields['zmq_pub_ip'] = self.get_ip_address('sbi_network', SDNControllerServiceInstance, 'zmq_pub_ip')
        fields['dp_comm_ip'] = self.get_ip_address('sbi_network', VSPGWUTenant, 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address('nbi_network', VSPGWCTenant, 'cp_comm_ip')
        fields['fpc_ip'] = self.get_ip_address('nbi_network', SDNControllerServiceInstance, 'fpc_ip')
        fields['cp_nb_server_ip'] = self.get_ip_address('nbi_network', VSPGWCTenant, 'cp_nb_server_ip')

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address('s11_network', VSPGWCTenant, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address('s1u_network', VSPGWUTenant, 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address('s11_network', VMMETenant, 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address('sgi_network', VENBServiceInstance, 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address('sgi_network', VSPGWUTenant, 'sgi_spgwu_ip')

        return fields

    def get_values_for_normal_scenario_wo_sdncontroller(self):
        fields = {}
        fields['scenario'] = "normal_scenario_without_sdncontroller"
        # for interface.cfg file
        fields['zmq_sub_ip'] = "127.0.0.1"
        fields['zmq_pub_ip'] = "127.0.0.1"
        fields['dp_comm_ip'] = self.get_ip_address('spgw_network', VSPGWUTenant, 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address('spgw_network', VSPGWCTenant, 'cp_comm_ip')
        fields['fpc_ip'] = "127.0.0.1"
        fields['cp_nb_server_ip'] = "127.0.0.1"

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address('s11_network', VSPGWCTenant, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address('s1u_network', VSPGWUTenant, 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address('s11_network', VMMETenant, 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address('sgi_network', VENBServiceInstance, 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address('sgi_network', VSPGWUTenant, 'sgi_spgwu_ip')

        return fields

    def get_values_for_emulator_scenario(self):
        fields = {}
        fields['scenario'] = "emulator_scenario"
        # for interface.cfg file
        fields['zmq_sub_ip'] = self.get_ip_address('sbi_network', SDNControllerServiceInstance, 'zmq_sub_ip')
        fields['zmq_pub_ip'] = self.get_ip_address('sbi_network', SDNControllerServiceInstance, 'zmq_pub_ip')
        fields['dp_comm_ip'] = self.get_ip_address('sbi_network', VSPGWUTenant, 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address('nbi_network', VSPGWCTenant, 'cp_comm_ip')
        fields['fpc_ip'] = self.get_ip_address('nbi_network', SDNControllerServiceInstance, 'fpc_ip')
        fields['cp_nb_server_ip'] = self.get_ip_address('nbi_network', VSPGWCTenant, 'cp_nb_server_ip')

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address('s11_network', VSPGWCTenant, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address('s1u_network', VSPGWUTenant, 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address('s11_network', VENBServiceInstance, 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address('sgi_network', VENBServiceInstance, 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address('sgi_network', VSPGWUTenant, 'sgi_spgwu_ip')

        return fields

    def get_values_for_emulator_scenario_wo_sdncontroller(self):
        fields = {}
        fields['scenario'] = "emulator_scenario_without_sdncontroller"
        # for interface.cfg file
        fields['zmq_sub_ip'] = "127.0.0.1"
        fields['zmq_pub_ip'] = "127.0.0.1"
        fields['dp_comm_ip'] = self.get_ip_address('spgw_network', VSPGWUTenant, 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address('spgw_network', VSPGWCTenant, 'cp_comm_ip')
        fields['fpc_ip'] = "127.0.0.1"
        fields['cp_nb_server_ip'] = "127.0.0.1"

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address('s11_network', VSPGWCTenant, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address('s1u_network', VSPGWUTenant, 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address('s11_network', VENBServiceInstance, 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address('sgi_network', VENBServiceInstance, 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address('sgi_network', VSPGWUTenant, 'sgi_spgwu_ip')

        return fields


    def has_venb(self):
        # try get vMME instance
        try:
            instance_id = self.get_instance_id(VENBServiceInstance)
        except Exception:
            self.log.debug('VENBServiceInstance not found')
            return False

        return True

    def has_vmme(self):
        # try get vMME instance
        try:
            instance_id = self.get_instance_id(VMMETenant)
        except Exception:
            self.log.debug('VMMETenant not found')
            return False

        return True

    def has_sdncontroller(self):
        # try get vMME instance
        try:
            instance_id = self.get_instance_id(SDNControllerServiceInstance)
        except Exception:
            self.log.debug('SDNControllerServiceInstance not found')
            return False

        return True

    def has_vspgwu(self):
        # try get vMME instance
        try:
            instance_id = self.get_instance_id(VSPGWUTenant)
        except Exception:
            self.log.debug('VSPGWUTenant instance not found')
            return False

        return True

    def has_internetemulator(self):
        # try get vMME instance
        try:
            instance_id = self.get_instance_id(InternetEmulatorServiceInstance)
        except Exception:
            self.log.debug('InternetEmulatorServiceInstance not found')
            return False

        return True


    def get_scenario(self):
        # try get vENB instance: one of both Spirent and NG4T
        venb_flag = self.has_venb()
        vmme_flag = self.has_vmme()
        sdncontroller_flag = self.has_sdncontroller()
        vspgwu_flag = self.has_vspgwu()
        internetemulator_flag = self.has_internetemulator()

        # wait until vspgwu and env are comming up
        while (not vspgwu_flag):
            print "wait -- vSPGWU has not been comming up"
            time.sleep(1)
            vspgwu_flag = self.has_vspgwu()

        while (not venb_flag):
            print "wait -- vENB has not been comming up"
            time.sleep(1)
            venb_flag = self.has_venb()

        if vmme_flag and venb_flag and sdncontroller_flag and vspgwu_flag and internetemulator_flag:
            return 'normal_scenario'

        if vmme_flag and venb_flag and (not sdncontroller_flag) and vspgwu_flag and internetemulator_flag:
            return 'normal_scenario_without_sdncontroller'

        if (not vmme_flag) and venb_flag and sdncontroller_flag and vspgwu_flag and (not internetemulator_flag):
            return 'emulator_scenario'

        if (not vmme_flag) and venb_flag and (not sdncontroller_flag) and vspgwu_flag and (not internetemulator_flag):
            return 'emulator_scenario_without_sdncontroller'

        return 'manual'

    # To get IP address
    def get_ip_address(self, network_name, service_instance, parameter):

        condition = False

        while (not condition):
            try:
                net_id = self.get_network_id(network_name)
                ins_id = self.get_instance_id(service_instance)
                ip_address = Port.objects.get(network_id=net_id, instance_id=ins_id).ip
                condition = True
            except Exception:
                ip_address = "error"
                self.log.error('Could not fetch parameter', parameter = parameter, network_name = network_name)

        return ip_address

    # To get each network id
    def get_network_id(self, network_name):
        return Network.objects.get(name=network_name).id

    # To get service_instance (assumption: there is a single instance for each service)
    def get_instance_id(self, serviceinstance):
        instances = serviceinstance.objects.all()
        instance_id = instances[0].instance_id
        return instance_id
