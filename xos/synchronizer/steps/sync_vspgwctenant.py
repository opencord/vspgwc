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
from django.db.models import Q, F
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

class SyncVSPGWCTenant(SyncInstanceUsingAnsible):
    provides = [VSPGWCTenant]

    observes = VSPGWCTenant

    requested_interval = 0

    template_name = "vspgwctenant_playbook.yaml"

    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncVSPGWCTenant, self).__init__(*args, **kwargs)

    def get_extra_attributes(self, o):
        if self.get_scenario() == 'manual':
            return self.get_extra_attributes_for_manual()

        fields = {}
        fields['scenario'] = self.get_scenario()
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

        # the parameter 's11_mme_ip' depends on scenarios
        if self.get_scenario() == 'ng4t':
            fields['s11_mme_ip'] = self.get_ip_address('s11_network', VMMETenant, 's11_mme_ip')
        elif self.get_scenario() == 'spirent':
            fields['s11_mme_ip'] = self.get_ip_address('s11_network', VENBServiceInstance, 's11_mme_ip')
        else:
            fields['s11_mme_ip'] = "scenario_error"

        return fields

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

        return fields

    def has_venb(self):
        # try get vMME instance
        try:
            instance_id = self.get_instance_id(VENBServiceInstance)
        except Exception:
            print 'cannot get VENBServiceInstance'
            return False

        return True

    def has_vmme(self):
        # try get vMME instance
        try:
            instance_id = self.get_instance_id(VMMETenant)
        except Exception:
            print 'cannot get VMMETenant'
            return False

        return True


    # Which scenario does it use among Spirent or NG4T?
    def get_scenario(self):
        # try get vENB instance: one of both Spirent and NG4T
        venb_flag = self.has_venb()
        vmme_flag = self.has_vmme()

        if vmme_flag:
            return 'ng4t'
        else:
            if venb_flag:
                return 'spirent'
            else:
                return 'manual'

    def get_ip_address(self, network_name, service_instance, parameter):

        if self.get_scenario() == 'manual':
            return "manual"

        try:
            net_id = self.get_network_id(network_name)
            ins_id = self.get_instance_id(service_instance)
            ip_address = Port.objects.get(network_id=net_id, instance_id=ins_id).ip

        except Exception:
            ip_address = "error"
            print "get failed -- %s" % (parameter)

        return ip_address

    # To get each network id
    def get_network_id(self, network_name):
        return Network.objects.get(name=network_name).id

    # To get service_instance (assumption: there is a single instance for each service)
    def get_instance_id(self, serviceinstance):
        instances = serviceinstance.objects.all()
        instance_id = instances[0].instance_id
        return instance_id
