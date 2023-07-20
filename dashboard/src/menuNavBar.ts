import { mdiAccount, mdiLogout, mdiThemeLightDark } from '@mdi/js'
import axios from 'axios'
import { flaskApiUrl } from './config'
import { MenuNavBarItem } from './interfaces'

const handleLogout = async () => {
  try {
    const token = JSON.parse(localStorage.getItem('token'))
    const config = {
      method: 'DELETE',
      url: `${flaskApiUrl}/auth`,
      data: { refresh_token: token.refresh_token },
    }
    await axios.request(config)
    localStorage.removeItem('token')
    localStorage.removeItem('expirationTime')
  } catch (error) {
    console.log(error)
  }
}

const menuNavBar: MenuNavBarItem[] = [
  {
    isCurrentUser: true,
    menu: [
      {
        icon: mdiAccount,
        label: 'My Profile',
        href: '/profile',
      },
      {
        isDivider: true,
      },
      {
        icon: mdiLogout,
        label: 'Log Out',
        isLogout: true,
        handler: handleLogout,
        href: '/login',
      },
    ],
  },
  {
    icon: mdiThemeLightDark,
    label: 'Light/Dark',
    isDesktopNoLabel: true,
    isToggleLightDark: true,
  },
]

export default menuNavBar
