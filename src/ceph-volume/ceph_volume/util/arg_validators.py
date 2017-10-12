import argparse
from ceph_volume.api import lvm


class LVPath(object):
    """
    A simple validator to ensure that a logical volume is specified like::

        <vg name>/<lv name>

    Because for LVM it is better to be specific on what group does an lv
    belongs to.

    Allow a vg group to be defined as well, since it is possible that a user
    may want to pass that so that lvm can carve out an LV.
    """

    def __call__(self, string):
        error = None
        if '/' not in string:
            # it is possible we have a volume group
            vg = lvm.get_vg(vg_name=string)
            if not vg:
                error = (
                    "Argument is not a volume group (allowed for bluestore) or a device. "
                    "Devices must be an absolute path. "
                    "For filestore argument must be volume_group/logical_volume"
                )
                raise argparse.ArgumentError(None, error)
            else:
                return string
        try:
            vg, lv = string.split('/')
        except ValueError:
            error = "Logical volume must be specified as 'volume_group/logical_volume' but got: %s" % string
            raise argparse.ArgumentError(None, error)

        if not vg:
            error = "Didn't specify a volume group like 'volume_group/logical_volume', got: %s" % string
        if not lv:
            error = "Didn't specify a logical volume like 'volume_group/logical_volume', got: %s" % string

        if error:
            raise argparse.ArgumentError(None, error)
        return string
