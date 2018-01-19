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

class ServiceGraphException(Exception):
    pass

class SyncVSPGWCTenant(SyncInstanceUsingAnsible):
    observes = VSPGWCTenant
    template_name = "vspgwctenant_playbook.yaml"
    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncVSPGWCTenant, self).__init__(*args, **kwargs)

    def get_extra_attributes(self, o):

        scenario = self.get_scenario(o)

        if scenario == 'cord_4_1_scenario':
            return self.get_values_for_CORD_4_1(o)
        elif scenario == 'cord_5_0_scenario':
            return self.get_values_for_CORD_5_0(o)
        else:
            return self.get_extra_attributes_for_manual(o)

    # fields for manual case
    def get_extra_attributes_for_manual(self, o):
        fields = {}
        fields['scenario'] = "manual"
        fields['cord_version'] = "manual"
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

    def get_values_for_CORD_4_1(self, o):
        fields = {}
        fields['cord_version'] = "4.1"
        fields['scenario'] = "cord_4_1_scenario"
        # for interface.cfg file
        fields['zmq_sub_ip'] = "127.0.0.1"
        fields['zmq_pub_ip'] = "127.0.0.1"
        fields['dp_comm_ip'] = self.get_ip_address_from_peer_service_instance(
            'spgw_network', "VSPGWUTenant", o, 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'spgw_network', o, o, 'cp_comm_ip')
        fields['fpc_ip'] = "127.0.0.1"
        fields['cp_nb_server_ip'] = "127.0.0.1"

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            's11_network', o, o, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address_from_peer_service_instance(
            's1u_network', "VSPGWUTenant", o, 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address_from_peer_service_instance(
            's11_network', "VENBServiceInstance", o, 's11_mme_ip')

        # for rules setup in ONOS
        fields['sgi_as_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VENBServiceInstance", o, 'sgi_as_ip')
        fields['sgi_spgwu_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VSPGWUTenant", o, 'sgi_spgwu_ip')

        return fields

    def get_values_for_CORD_5_0(self, o):
        fields = {}
        fields['cord_version'] = "5.0"
        fields['scenario'] = "cord_5_0_scenario"

        # for interface.cfg file
        fields['zmq_sub_ip'] = "127.0.0.1"
        fields['zmq_pub_ip'] = "127.0.0.1"
        fields['dp_comm_ip'] = self.get_ip_address_from_peer_service_instance(
            'spgw_network', "VSPGWUTenant", o, 'dp_comm_ip')
        fields['cp_comm_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            'spgw_network', o, o, 'cp_comm_ip')
        fields['fpc_ip'] = "127.0.0.1"
        fields['cp_nb_server_ip'] = "127.0.0.1"

        # for cp_config.cfg file
        fields['s11_sgw_ip'] = self.get_ip_address_from_peer_service_instance_instance(
            's11_network', o, o, 's11_sgw_ip')
        fields['s1u_sgw_ip'] = self.get_ip_address_from_peer_service_instance(
            's1u_network', "VSPGWUTenant", o, 's1u_sgw_ip')
        fields['s11_mme_ip'] = self.get_ip_address_from_peer_service_instance(
            's11_network', "VMMETenant", o, 's11_mme_ip')

        # for rules setup in ONOS
        internetemulator_flag = self.has_instance("InternetEmulatorServiceInstance", o)
        if (internetemulator_flag):
            fields['sgi_as_ip'] = self.get_ip_address_from_peer_service_instance(
                'sgi_network', "InternetEmulatorServiceInstance", o, 'sgi_as_ip')
        else:
            fields['sgi_as_ip'] = o.appserver_ip_addr
        fields['sgi_spgwu_ip'] = self.get_ip_address_from_peer_service_instance(
            'sgi_network', "VSPGWUTenant", o, 'sgi_spgwu_ip')

        return fields


    def get_scenario(self, o):
        venb_flag = self.has_instance("VENBServiceInstance", o)
        vmme_flag = self.has_instance("VMMETenant", o)
        sdncontroller_flag = self.has_instance(
            "SDNControllerServiceInstance", o)
        vspgwu_flag = self.has_instance("VSPGWUTenant", o)
        internetemulator_flag = self.has_instance(
            "InternetEmulatorServiceInstance", o)
        vhss_flag = self.has_instance("VHSSTenant", o)
        hssdb_flag = self.has_instance("HSSDBServiceInstance", o)

        if (o.blueprint == "build") or (o.blueprint == "MCORD 4.1"):
            if not venb_flag:
                self.defer_sync(o, "Waiting for eNB image to become available")
            if not vspgwu_flag:
                self.defer_sync(o, "Waiting for SPGWU image to become available")
            return 'cord_4_1_scenario'

        if (o.blueprint == "mcord_5") or (o.blueprint == "MCORD 5"):
            if not hssdb_flag:
                self.defer_sync(o, "Waiting for HSS_DB image to become available")
            if not vhss_flag:
                self.defer_sync(o, "Waiting for vHSS image to become available")
            if not vmme_flag:
                self.defer_sync(o, "Waiting for vMME image to become available")
            if not vspgwu_flag:
                self.defer_sync(o, "Waiting for vSPGWU image to become available")
            return 'cord_5_0_scenario'

        return 'manual'

    def get_ip_address_from_peer_service_instance(self, network_name, sitype, o, parameter=None):
        peer_si = self.get_peer_serviceinstance_of_type(sitype, o)
        return self.get_ip_address_from_peer_service_instance_instance(network_name, peer_si, o, parameter)

    def get_ip_address_from_peer_service_instance_instance(self, network_name, peer_si, o, parameter=None):
        try:
            net_id = self.get_network_id(network_name)
            ins_id = peer_si.leaf_model.instance_id
            ip_address = Port.objects.get(
                network_id=net_id, instance_id=ins_id).ip
        except Exception:
            self.log.error("Failed to fetch parameter",
                           parameter=parameter,
                           network_name=network_name)
            self.defer_sync(o, "Waiting for parameters to become available")

        return ip_address

    def get_peer_serviceinstance_of_type(self, sitype, o):
        prov_link_set = ServiceInstanceLink.objects.filter(
            subscriber_service_instance_id=o.id)

        try:
            peer_service = next(
                p.provider_service_instance for p in prov_link_set if p.provider_service_instance.leaf_model_name == sitype)
        except StopIteration:
            sub_link_set = ServiceInstanceLink.objects.filter(
                provider_service_instance_id=o.id)
            try:
                peer_service = next(
                    s.subscriber_service_instance for s in sub_link_set if s.subscriber_service_instance.leaf_model_name == sitype)
            except StopIteration:
                self.log.error(
                    'Could not find service type in service graph', service_type=sitype, object=o)
                raise ServiceGraphException(
                    "Synchronization failed due to incomplete service graph")

        return peer_service 

    # To get each network id
    def get_network_id(self, network_name):
        return Network.objects.get(name=network_name).id

    # To get service_instance (assumption: there is a single instance for each service)
    def get_instance_id(self, serviceinstance):
        instances = serviceinstance.objects.all()
        instance_id = instances[0].instance_id
        return instance_id

    def has_instance(self, sitype, o):
        try:
            i = self.get_peer_serviceinstance_of_type(sitype, o)
        except ServiceGraphException:
            self.log.info("Missing in ServiceInstance graph",
                          serviceinstance=sitype)
            return False

        return i.leaf_model.instance_id
