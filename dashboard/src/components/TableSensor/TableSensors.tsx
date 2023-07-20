import { mdiEye, mdiTrashCan } from '@mdi/js'
import BaseButton from '../BaseButton'
import BaseButtons from '../BaseButtons'
import CardBox from '../CardBox'
import CardBoxComponentEmpty from '../CardBoxComponentEmpty'
import CardBoxModal from '../CardBoxModal'

interface Sensor {
  id: string
  ip_address: string
  name: string
  created_at: string
}

type Props = {
  sensors: Sensor[]
  status: object
  id: string
  currentPage: number
  isModalTrashActive: boolean
  isSubmitting: boolean
  modalConfirm: () => void
  modalCancel: () => void
  modalDelete: (id: string) => void
  pageChange: (page: number) => void
}

const TableSensors = (props: Props) => {
  const perPage = 5
  const sensorsPaginated = props.sensors.slice(
    perPage * props.currentPage,
    perPage * (props.currentPage + 1)
  )
  const numPages = Math.ceil(props.sensors.length / perPage)
  const pagesList = []

  for (let i = 0; i < numPages; i++) {
    pagesList.push(i)
  }

  return (
    <>
      <CardBoxModal
        isSubmitting={props.isSubmitting}
        title="Delete Confirmation"
        buttonColor="danger"
        buttonLabel="Confirm"
        isActive={props.isModalTrashActive}
        onConfirm={props.modalConfirm}
        onCancel={props.modalCancel}
      >
        <p>Are you sure you want to delete this sensor?</p>
      </CardBoxModal>

      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Name</th>
            <th>Created At</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {sensorsPaginated.map((sensor, index) => (
            <tr key={index}>
              <td data-label="IP Address">{sensor.ip_address}</td>
              <td data-label="Name">{sensor.name}</td>
              <td data-label="Created At">{new Date(sensor.created_at).toLocaleString()}</td>
              <td data-label="Action " className="before:hidden lg:w-1 whitespace-nowrap">
                <BaseButtons type="justify-start lg:justify-end" noWrap>
                  <BaseButton
                    color="info"
                    icon={mdiEye}
                    small
                    outline
                    href="/sensors/[id]"
                    as={`/sensors/${sensor.id}`}
                  />
                  <BaseButton
                    color="danger"
                    icon={mdiTrashCan}
                    onClick={() => props.modalDelete(sensor.id)}
                    small
                    outline
                  />
                </BaseButtons>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {props.sensors.length === 0 && (
        <CardBox>
          <CardBoxComponentEmpty />
        </CardBox>
      )}
      {props.sensors.length > 0 && (
        <>
          <div className="p-3 lg:px-6 border-t border-gray-100 dark:border-slate-800">
            <div className="flex flex-col md:flex-row items-center justify-between py-3 md:py-0">
              <BaseButtons>
                {pagesList.map((page) => (
                  <BaseButton
                    key={page}
                    active={page === props.currentPage}
                    label={page + 1}
                    color={page === props.currentPage ? 'lightDark' : 'whiteDark'}
                    small
                    onClick={() => props.pageChange(page)}
                  />
                ))}
              </BaseButtons>
              <small className="mt-6 md:mt-0">
                Page {props.currentPage + 1} of {numPages}
              </small>
            </div>
          </div>
        </>
      )}
    </>
  )
}

export default TableSensors
