import React from 'react'
import { mdiLogout, mdiClose } from '@mdi/js'
import BaseIcon from './BaseIcon'
import AsideMenuItem from './AsideMenuItem'
import AsideMenuList from './AsideMenuList'
import { MenuAsideItem } from '../interfaces'
import { useAppSelector } from '../stores/hooks'
import axios from 'axios'
import { flaskApiUrl } from '../config'
import Image from 'next/image'
import logo from '../../public/logo.png'

type Props = {
  menu: MenuAsideItem[]
  roles: string
  className?: string
  onAsideLgCloseClick: () => void
}

export default function AsideMenuLayer({ menu, className = '', ...props }: Props) {
  const asideStyle = useAppSelector((state) => state.style.asideStyle)
  const asideBrandStyle = useAppSelector((state) => state.style.asideBrandStyle)
  const asideScrollbarsStyle = useAppSelector((state) => state.style.asideScrollbarsStyle)
  const darkMode = useAppSelector((state) => state.style.darkMode)

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

  const logoutItem: MenuAsideItem = {
    label: 'Logout',
    icon: mdiLogout,
    color: 'info',
    isLogout: true,
    href: '/login',
    isAdmin: false,
    handler: handleLogout,
  }

  const handleAsideLgCloseClick = (e: React.MouseEvent) => {
    e.preventDefault()
    props.onAsideLgCloseClick()
  }

  return (
    <aside
      className={`${className} zzz lg:py-2 lg:pl-2 w-60 fixed flex z-40 top-0 h-screen transition-position overflow-hidden`}
    >
      <div
        className={`lg:rounded-2xl flex-1 flex flex-col overflow-hidden dark:bg-slate-900 ${asideStyle}`}
      >
        <div
          className={`flex flex-row h-14 items-center justify-between dark:bg-slate-900 ${asideBrandStyle} mb-5`}
        >
          <div className="text-center flex-1 lg:text-left lg:pl-6 xl:text-center xl:pl-0">
            <div className="grid justify-items-center pt-5">
              <Image src={logo} width={150} alt="" />
            </div>
          </div>
          <button
            className="hidden lg:inline-block xl:hidden p-3"
            onClick={handleAsideLgCloseClick}
          >
            <BaseIcon path={mdiClose} />
          </button>
        </div>
        <div
          className={`flex-1 overflow-y-auto overflow-x-hidden ${
            darkMode ? 'aside-scrollbars-[slate]' : asideScrollbarsStyle
          }`}
        >
          <AsideMenuList menu={menu} roles={props.roles} />
        </div>
        <ul>
          <AsideMenuItem item={logoutItem} roles={props.roles} />
        </ul>
      </div>
    </aside>
  )
}
