import React from 'react'
import { MenuAsideItem } from '../interfaces'
import AsideMenuItem from './AsideMenuItem'

type Props = {
  menu: MenuAsideItem[]
  isDropdownList?: boolean
  className?: string
  roles?: string
}

export default function AsideMenuList({
  menu,
  isDropdownList = false,
  className = '',
  roles,
}: Props) {
  return (
    <ul className={className}>
      {menu.map((item, index) => (
        <AsideMenuItem key={index} item={item} isDropdownList={isDropdownList} roles={roles} />
      ))}
    </ul>
  )
}
