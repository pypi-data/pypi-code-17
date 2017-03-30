# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of kiwi.
#
# kiwi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi.  If not, see <http://www.gnu.org/licenses/>
#
import os
import platform

# project
from kiwi.bootloader.install.base import BootLoaderInstallBase
from kiwi.command import Command
from kiwi.logger import log
from kiwi.defaults import Defaults
from kiwi.mount_manager import MountManager
from kiwi.path import Path

from kiwi.exceptions import (
    KiwiBootLoaderGrubInstallError,
    KiwiBootLoaderGrubPlatformError,
    KiwiBootLoaderGrubDataError
)


class BootLoaderInstallGrub2(BootLoaderInstallBase):
    """
    grub2 bootloader installation

    Attributes

    * :attr:`arch`
        platform.machine

    * :attr:`firmware`
        Instance of FirmWare

    * :attr:`efi_mount`
        Instance of MountManager for EFI device

    * :attr:`root_mount`
        Instance of MountManager for root device

    * :attr:`boot_mount`
        Instance of MountManager for boot device

    * :attr:`device_mount`
        Instance of MountManager for /dev tree

    * :attr:`proc_mount`
        Instance of MountManager for proc

    * :attr:`sysfs_mount`
        Instance of MountManager for sysfs
    """
    def post_init(self, custom_args):
        """
        grub2 post initialization method

        Setup class attributes
        """
        self.arch = platform.machine()
        self.custom_args = custom_args
        self.install_arguments = []
        self.firmware = None
        self.efi_mount = None
        self.root_mount = None
        self.boot_mount = None
        self.device_mount = None
        self.proc_mount = None
        self.sysfs_mount = None
        self.volumes = None
        self.volumes_mount = []
        self.target_removable = None
        if custom_args and 'target_removable' in custom_args:
            self.target_removable = custom_args['target_removable']
        if custom_args and 'system_volumes' in custom_args:
            self.volumes = custom_args['system_volumes']
        if custom_args and 'firmware' in custom_args:
            self.firmware = custom_args['firmware']

        if self.firmware and self.firmware.efi_mode():
            if not custom_args or 'efi_device' not in custom_args:
                raise KiwiBootLoaderGrubInstallError(
                    'EFI device name required for shim installation'
                )
        if not custom_args or 'boot_device' not in custom_args:
            raise KiwiBootLoaderGrubInstallError(
                'boot device name required for grub2 installation'
            )
        if not custom_args or 'root_device' not in custom_args:
            raise KiwiBootLoaderGrubInstallError(
                'root device name required for grub2 installation'
            )

    def install_required(self):
        """
        Check if grub2 has to be installed

        Take architecture and firmware setup into account to check if
        bootloader code in a boot record is required

        :rtype: bool
        """
        if 'ppc64' in self.arch and self.firmware.opal_mode():
            # OPAL doesn't need a grub2 stage1, just a config file.
            # The machine will be setup to kexec grub2 in user space
            log.info(
                'No grub boot code installation in opal mode on %s', self.arch
            )
            return False
        elif 'arm' in self.arch or self.arch == 'aarch64':
            # On arm grub2 is used for EFI setup only, no install
            # of grub2 boot code makes sense
            log.info(
                'No grub boot code installation on %s', self.arch
            )
            return False
        return True

    def install(self):
        """
        Install bootloader on disk device
        """
        log.info('Installing grub2 on disk %s', self.device)

        if self.target_removable:
            self.install_arguments.append('--removable')

        if self.arch == 'x86_64' or self.arch == 'i686' or self.arch == 'i586':
            self.target = 'i386-pc'
            self.install_device = self.device
            self.modules = ' '.join(
                Defaults.get_grub_bios_modules(multiboot=True)
            )
            self.install_arguments.append('--skip-fs-probe')
        elif self.arch.startswith('ppc64'):
            if not self.custom_args or 'prep_device' not in self.custom_args:
                raise KiwiBootLoaderGrubInstallError(
                    'prep device name required for grub2 installation on ppc'
                )
            self.target = 'powerpc-ieee1275'
            self.install_device = self.custom_args['prep_device']
            self.modules = ' '.join(Defaults.get_grub_ofw_modules())
            self.install_arguments.append('--skip-fs-probe')
            self.install_arguments.append('--no-nvram')
        else:
            raise KiwiBootLoaderGrubPlatformError(
                'host architecture %s not supported for grub2 install' %
                self.arch
            )

        self.root_mount = MountManager(
            device=self.custom_args['root_device']
        )
        self.boot_mount = MountManager(
            device=self.custom_args['boot_device'],
            mountpoint=self.root_mount.mountpoint + '/boot'
        )

        self.root_mount.mount()

        if not self.root_mount.device == self.boot_mount.device:
            self.boot_mount.mount()

        if self.volumes:
            for volume_path in Path.sort_by_hierarchy(
                sorted(self.volumes.keys())
            ):
                volume_mount = MountManager(
                    device=self.volumes[volume_path]['volume_device'],
                    mountpoint=self.root_mount.mountpoint + '/' + volume_path
                )
                self.volumes_mount.append(volume_mount)
                volume_mount.mount(
                    options=[self.volumes[volume_path]['volume_options']]
                )

        self.device_mount = MountManager(
            device='/dev',
            mountpoint=self.root_mount.mountpoint + '/dev'
        )
        self.proc_mount = MountManager(
            device='/proc',
            mountpoint=self.root_mount.mountpoint + '/proc'
        )
        self.sysfs_mount = MountManager(
            device='/sys',
            mountpoint=self.root_mount.mountpoint + '/sys'
        )
        self.device_mount.bind_mount()
        self.proc_mount.bind_mount()
        self.sysfs_mount.bind_mount()

        # check if a grub installation could be found in the image system
        grub_directory = Defaults.get_grub_path(
            self.root_mount.mountpoint + '/usr/lib'
        )
        if not grub_directory:
            raise KiwiBootLoaderGrubDataError(
                'No grub2 installation found in %s' % self.root_mount.mountpoint
            )
        grub_directory = grub_directory.replace(
            self.root_mount.mountpoint, ''
        )
        module_directory = grub_directory + '/' + self.target
        boot_directory = '/boot'

        # wipe existing grubenv to allow grub2-install to create a new one
        Path.wipe(
            os.sep.join(
                [self.root_mount.mountpoint, 'boot', 'grub2', 'grubenv']
            )
        )
        # install grub2 boot code
        Command.run(
            [
                'chroot', self.root_mount.mountpoint, 'grub2-install'
            ] + self.install_arguments + [
                '--directory', module_directory,
                '--boot-directory', boot_directory,
                '--target', self.target,
                '--modules', self.modules,
                self.install_device
            ]
        )

        if self.firmware and self.firmware.efi_mode() == 'uefi':
            self.efi_mount = MountManager(
                device=self.custom_args['efi_device'],
                mountpoint=self.root_mount.mountpoint + '/boot/efi'
            )
            self.efi_mount.mount()

            # Before we call shim-install, the grub2-install binary is
            # replaced by a noop. Actually there is no reason for shim-install
            # to call grub2-install because it should only setup the system
            # for EFI secure boot which does not require any bootloader code
            # in the master boot record. In addition kiwi has called
            # grub2-install right before
            self._disable_grub2_install(self.root_mount.mountpoint)
            Command.run(
                [
                    'chroot', self.root_mount.mountpoint,
                    'shim-install', '--removable',
                    self.install_device
                ]
            )
            # restore the grub2-install noop
            self._enable_grub2_install(self.root_mount.mountpoint)

    def _disable_grub2_install(self, root_path):
        grub2_install = ''.join(
            [root_path, '/usr/sbin/grub2-install']
        )
        grub2_install_backup = ''.join(
            [root_path, '/usr/sbin/grub2-install.orig']
        )
        grub2_install_noop = ''.join(
            [root_path, '/bin/true']
        )
        Command.run(
            ['cp', '-p', grub2_install, grub2_install_backup]
        )
        Command.run(
            ['cp', grub2_install_noop, grub2_install]
        )

    def _enable_grub2_install(self, root_path):
        grub2_install = ''.join(
            [root_path, '/usr/sbin/grub2-install']
        )
        grub2_install_backup = ''.join(
            [root_path, '/usr/sbin/grub2-install.orig']
        )
        if os.path.exists(grub2_install_backup):
            Command.run(
                ['cp', '-p', grub2_install_backup, grub2_install]
            )

    def __del__(self):
        log.info('Cleaning up %s instance', type(self).__name__)
        for volume_mount in reversed(self.volumes_mount):
            volume_mount.umount()
        if self.device_mount:
            self.device_mount.umount()
        if self.proc_mount:
            self.proc_mount.umount()
        if self.sysfs_mount:
            self.sysfs_mount.umount()
        if self.efi_mount:
            self.efi_mount.umount()
        if self.boot_mount:
            self.boot_mount.umount()
        if self.root_mount:
            self._enable_grub2_install(self.root_mount.mountpoint)
            self.root_mount.umount()
