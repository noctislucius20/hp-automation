import { mdiMonitor, mdiPackage } from '@mdi/js'
import { MenuAsideItem } from './interfaces'

const menuAside: MenuAsideItem[] = [
  {
    href: '/dashboard',
    icon: mdiMonitor,
    label: 'Dashboard',
    isAdmin: false,
  },
  {
    label: 'Resources',
    icon: mdiPackage,
    menu: [
      {
        label: 'Sensors',
        href: '/sensors/overview',
        isAdmin: false,
      },
      {
        label: 'Honeypots',
        href: '/honeypots/overview',
        isAdmin: true,
      },
      {
        label: 'Users',
        href: '/users/overview',
        isAdmin: true,
      },
    ],
    isAdmin: false,
  },
]

export default menuAside
