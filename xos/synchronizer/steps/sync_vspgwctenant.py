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

        scenario = self.get_scenario(o)

        if scenario == 'normal_scenario':
            return self.get_values_for_normal_scenario(o)
        elif scenario == 'normal_scenario_without_sdncontroller':
            return self.get_values_for_normal_scenario_wo_sdncontroller(o)
        elif scenario == 'emulator_scenario':
            return self.get_values_for_emulator_scenario(o)
        elif scenario == 'emulator_scenario_without_sdncontroller':
            return self.get_values_for_emulator_scenario_wo_sdncontroller(o)
        else:
            return self.get_extra_attributes_for_manual(o)

    # fields for manual case
    def get_extra_attributes_for_manual(self, o):
        fields = {}
        fields['scenario'] = self.get_scenario(o)
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

    def get_values_for_normal_scenario(self, o):
        fields = {}
        fields['scenario'] = "normal_scenario"
        # for interface.cfg file
        fields['zmq_sub_ip'] = self.get_ip_address_from_peer_service_instance(
            'sbi_network', "SDNControllerServiceInstance", 'zmq_sub_ip')
        fields['zmq_pub_ip'] = self.get_ip_address_from_peer_service_instance(
            'sbi_network', "SDNControllerServiceInstance", 'zmq_pub_ip')
        fields['dp_comm_ip'] = self.get_ip_address_from_peer_service_instance(
            'sbi_network', "VSPGWUTenant", 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'nbi_network', o, 'cp_comm_ip')
        fields['fpc_ip'] = self.get_ip_address_from_peer_service_instance(
            'nbi_network', "SDNControllerServiceInstance", 'fpc_ip')
        fields['cp_nb_server_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'nbi_network', o, 'cp_nb_server_ip')

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            's11_network', o, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address_from_peer_service_instance(
            's1u_network', "VSPGWUTenant", 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address_from_peer_service_instance(
            's11_network', "VMMETenant", 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VENBServiceInstance", 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VSPGWUTenant", 'sgi_spgwu_ip')

        return fields

    def get_values_for_normal_scenario_wo_sdncontroller(self, o):
        fields = {}
        fields['scenario'] = "normal_scenario_without_sdncontroller"
        # for interface.cfg file
        fields['zmq_sub_ip'] = "127.0.0.1"
        fields['zmq_pub_ip'] = "127.0.0.1"
        fields['dp_comm_ip'] = self.get_ip_address_from_peer_service_instance(
            'spgw_network', "VSPGWUTenant", 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'spgw_network', o, 'cp_comm_ip')
        fields['fpc_ip'] = "127.0.0.1"
        fields['cp_nb_server_ip'] = "127.0.0.1"

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            's11_network', o, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address_from_peer_service_instance(
            's1u_network', "VSPGWUTenant", 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address_from_peer_service_instance(
            's11_network', "VMMETenant", 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VENBServiceInstance", 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VSPGWUTenant", 'sgi_spgwu_ip')

        return fields

    def get_values_for_emulator_scenario(self, o):
        fields = {}
        fields['scenario'] = "emulator_scenario"
        # for interface.cfg file
        fields['zmq_sub_ip'] = self.get_ip_address_from_peer_service_instance(
            'sbi_network', "SDNControllerServiceInstance", 'zmq_sub_ip')
        fields['zmq_pub_ip'] = self.get_ip_address_from_peer_service_instance(
            'sbi_network', "SDNControllerServiceInstance", 'zmq_pub_ip')
        fields['dp_comm_ip'] = self.get_ip_address_from_peer_service_instance(
            'sbi_network', "VSPGWUTenant", 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'nbi_network', o, 'cp_comm_ip')
        fields['fpc_ip'] = self.get_ip_address_from_peer_service_instance(
            'nbi_network', "SDNControllerServiceInstance", 'fpc_ip')
        fields['cp_nb_server_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'nbi_network', o, 'cp_nb_server_ip')

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            's11_network', o, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address_from_peer_service_instance(
            's1u_network', "VSPGWUTenant", 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address_from_peer_service_instance(
            's11_network', "VENBServiceInstance", 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VENBServiceInstance", 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VSPGWUTenant", 'sgi_spgwu_ip')

        return fields

    def get_values_for_emulator_scenario_wo_sdncontroller(self, o):
        fields = {}
        fields['scenario'] = "emulator_scenario_without_sdncontroller"
        # for interface.cfg file
        fields['zmq_sub_ip'] = "127.0.0.1"
        fields['zmq_pub_ip'] = "127.0.0.1"
        fields['dp_comm_ip'] = self.get_ip_address_from_peer_service_instance(
            'spgw_network', "VSPGWUTenant", 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'spgw_network', o, 'cp_comm_ip')
        fields['fpc_ip'] = "127.0.0.1"
        fields['cp_nb_server_ip'] = "127.0.0.1"

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            's11_network', o, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address_from_peer_service_instance(
            's1u_network', "VSPGWUTenant", 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address_from_peer_service_instance(
            's11_network', "VENBServiceInstance", 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VENBServiceInstance", 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VSPGWUTenant", 'sgi_spgwu_ip')

        return fields

    def get_scenario(self, o):
        venb_flag = self.has_instance("VENBServiceInstance", o)
        vmme_flag = self.has_instance("VMMETenant", o)
        sdncontroller_flag = self.has_instance(
            "SDNControllerServiceInstance", o)
        vspgwu_flag = self.has_instance("VSPGWUTenant", o)
        internetemulator_flag = self.has_instance(
            "SDNControllerServiceInstance", o)

        if vmme_flag and venb_flag and sdncontroller_flag and vspgwu_flag and internetemulator_flag:
            return 'ng4t_with_sdncontroller'

        if vmme_flag and venb_flag and (not sdncontroller_flag) and vspgwu_flag and internetemulator_flag:
            return 'ng4t_without_sdncontroller'

        if (not vmme_flag) and venb_flag and sdncontroller_flag and vspgwu_flag and (not internetemulator_flag):
            return 'spirent_with_sdncontroller'

        if (not vmme_flag) and venb_flag and (not sdncontroller_flag) and vspgwu_flag and (
                not internetemulator_flag):
            return 'spirent_without_sdncontroller'

        return 'manual'

    def get_ip_address_from_peer_service_instance(self, network_name, sitype, o, parameter=None):
        peer_si = self.get_peer_serviceinstance_of_type(sitype, o)
        return self.get_ip_address_for_peer_service_instance_instance(network_name, peer_si, parameter)

    def get_ip_address_from_peer_service_instance_instance(self, network_name, peer_si, parameter=None):
        try:
            net_id = self.get_network_id(network_name)
            ins_id = peer_si.instance_id
            ip_address = Port.objects.get(
                network_id=net_id, instance_id=ins_id).ip
        except Exception:
            self.log.error("Failed to fetch parameter",
                           parameter=parameter,
                           network_name=network_name)
            self.defer_sync("Waiting for parameters to become available")

        return ip_address

    def get_peer_serviceinstance_of_type(self, sitype, o):
        prov_link_set = ServiceInstanceLink.objects.filter(
            subscriber_service_instance_id=o.id)

        try:
            peer_service = next(
                p for p in prov_link_set if p.leaf_model_name == sitype)
        except StopIteration:
            sub_link_set = ServiceInstanceLink.objects.filter(
                provider_service_instance_id=o.id)
            try:
                peer_service = next(
                    s for s in sub_link_set if s.leaf_model_name == sitype)
            except StopIteration:
                self.log.error(
                    'Could not find service type in service graph', service_type=sitype, object=o)
                raise Exception(
                    "Synchronization failed due to incomplete service graph")

        return peer_service

    # To get IP address
    def get_ip_address_from_peer_service_instance(self, network_name, service_instance, parameter):
        condition = False

        while (not condition):
            try:
                net_id = self.get_network_id(network_name)
                ins_id = self.get_instance_id(service_instance)
                ip_address = Port.objects.get(
                    network_id=net_id, instance_id=ins_id).ip
                condition = True
            except Exception:
                ip_address = "error"
                self.log.error('Could not fetch parameter',
                               parameter=parameter, network_name=network_name)
                self.defer_sync("Waiting for parameters to become available")

        return ip_address

    # To get each network id
    def get_network_id(self, network_name):
        return Network.objects.get(name=network_name).id

    # To get service_instance (assumption: there is a single instance for each service)
    def get_instance_id(self, serviceinstance):
        instances = serviceinstance.objects.all()
        instance_id = instances[0].instance_id
        return instance_id

    def has_instance(self, sitype, o):
        i = self.get_peer_serviceinstance_of_type(sitype, o)
        if not i:
            self.log.info("Missing in ServiceInstance graph",
                          serviceinstance=sitype)
            return False

        return i.instance_id
