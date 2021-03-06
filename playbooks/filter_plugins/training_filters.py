#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: expandtab:tabstop=4:shiftwidth=4
# pylint: disable=missing-docstring, no-self-use, too-few-public-methods

from ansible import errors
import copy

def oo_subnets_from_zones(zones, network_prefix, cluster_id):
    ''' This filter plugin will create a ec2_vpc subnets list from a list of
        zones
    '''
    if not issubclass(type(zones), list):
        raise errors.AnsibleFilterError("|failed expects to filter on a list")
    result = []
    for i, zone in enumerate(zones):
        z_info = dict(
                cidr = "{0}{1}.0/24".format(network_prefix, i),
                az = zone,
                resource_tags = dict(
                    env = cluster_id,
                    Name = "{0}-subnet-{1}".format(cluster_id, i)
                )
        )
        result.append(z_info)

    return result


def oo_dict_merge(data, dict_to_merge):
    ''' This filter plugin will merge two dicts.
    '''
    if not issubclass(type(data), dict):
        raise errors.AnsibleFilterError("|failed expects to filter on a dict")
    if not issubclass(type(dict_to_merge), dict):
        raise errors.AnsibleFilterError("|failed expects dict_to_merge to be a dict")

    new_dict = copy.deepcopy(data)

    for key, value in dict_to_merge.iteritems():
        new_dict[key] = copy.deepcopy(value)

    return new_dict


class FilterModule(object):
    def filters(self):
        return {
            "oo_dict_merge": oo_dict_merge,
            "oo_subnets_from_zones": oo_subnets_from_zones
        }
