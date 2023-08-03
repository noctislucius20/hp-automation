import React from 'react'
import type { ReactElement } from 'react'
import Head from 'next/head'
import BaseButton from '../../components/BaseButton'
import CardBox from '../../components/CardBox'
import SectionFullScreen from '../../components/SectionFullScreen'
import { getPageTitle } from '../../config'
import LayoutGuest from '../../layouts/Guest'

export default function Error() {
  return (
    <>
      <Head>
        <title>{getPageTitle('Error')}</title>
      </Head>

      <SectionFullScreen bg="pinkRed">
        <CardBox
          className="w-11/12 md:w-7/12 lg:w-6/12 xl:w-4/12 shadow-2xl"
          footer={<BaseButton href="/dashboard" label="Back to Dashboard" color="danger" />}
        >
          <div className="space-y-3">
            <h1 className="text-2xl">Access Forbidden</h1>

            <p>You&apos;re not allowed to access this resource</p>
          </div>
        </CardBox>
      </SectionFullScreen>
    </>
  )
}

Error.getLayout = function getLayout(page: ReactElement) {
  return <LayoutGuest>{page}</LayoutGuest>
}
