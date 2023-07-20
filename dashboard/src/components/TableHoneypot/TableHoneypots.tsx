import { mdiEye, mdiTrashCan } from '@mdi/js'
import BaseButton from '../BaseButton'
import BaseButtons from '../BaseButtons'
import CardBox from '../CardBox'
import CardBoxComponentEmpty from '../CardBoxComponentEmpty'
import CardBoxModal from '../CardBoxModal'

interface Honeypot {
  id: string
  name: string
  description: string
  created_at: string
}

type Props = {
  honeypots: Honeypot[]
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

const TableHoneypots = (props: Props) => {
  const perPage = 5
  const honeypotsPaginated = props.honeypots.slice(
    perPage * props.currentPage,
    perPage * (props.currentPage + 1)
  )
  const numPages = Math.ceil(props.honeypots.length / perPage)
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
        <p>Are you sure you want to delete this honeypot?</p>
      </CardBoxModal>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Created At</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {honeypotsPaginated.map((honeypot, index) => (
            <tr key={index}>
              <td data-label="Name">{honeypot.name}</td>
              <td data-label="Description">{honeypot.description}</td>
              <td data-label="Created At">{new Date(honeypot.created_at).toLocaleString()}</td>
              <td data-label="Action " className="before:hidden lg:w-1 whitespace-nowrap">
                <BaseButtons type="justify-start lg:justify-end" noWrap>
                  <BaseButton
                    color="info"
                    icon={mdiEye}
                    small
                    outline
                    href="/honeypots/[id]"
                    as={`/honeypots/${honeypot.id}`}
                  />
                  <BaseButton
                    color="danger"
                    icon={mdiTrashCan}
                    onClick={() => props.modalDelete(honeypot.id)}
                    small
                    outline
                  />
                </BaseButtons>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {props.honeypots.length === 0 && (
        <CardBox>
          <CardBoxComponentEmpty />
        </CardBox>
      )}
      {props.honeypots.length > 0 && (
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

export default TableHoneypots
