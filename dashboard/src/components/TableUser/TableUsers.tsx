import { mdiEye, mdiTrashCan } from '@mdi/js'
import BaseButton from '../BaseButton'
import BaseButtons from '../BaseButtons'
import CardBox from '../CardBox'
import CardBoxComponentEmpty from '../CardBoxComponentEmpty'
import CardBoxModal from '../CardBoxModal'

interface User {
  username: string
  roles: string
  created_at: string
}

type Props = {
  users: User[]
  status: object
  id: string
  currentPage: number
  isModalTrashActive: boolean
  isSubmitting: boolean
  currentUser: string
  modalConfirm: () => void
  modalCancel: () => void
  modalDelete: (id: string) => void
  pageChange: (page: number) => void
}

const TableUsers = (props: Props) => {
  const perPage = 5
  const usersPaginated = props.users.slice(
    perPage * props.currentPage,
    perPage * (props.currentPage + 1)
  )
  const numPages = Math.ceil(props.users.length / perPage)
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
        <p>Are you sure you want to delete this user?</p>
      </CardBoxModal>

      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>Roles</th>
            <th>Created At</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {usersPaginated
            .filter((user) => user.username !== props.currentUser)
            .map((user, index) => (
              <tr key={index}>
                <td data-label="Username">{user.username}</td>
                <td data-label="Roles">{user.roles}</td>
                <td data-label="Created At">{new Date(user.created_at).toLocaleString()}</td>
                <td data-label="Action " className="before:hidden lg:w-1 whitespace-nowrap">
                  <BaseButtons type="justify-start lg:justify-end" noWrap>
                    <BaseButton
                      color="info"
                      icon={mdiEye}
                      small
                      outline
                      href="/users/[username]"
                      as={`/users/${user.username}`}
                    />
                    <BaseButton
                      color="danger"
                      icon={mdiTrashCan}
                      onClick={() => props.modalDelete(user.username)}
                      small
                      outline
                    />
                  </BaseButtons>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
      {props.users.length < 2 && (
        <CardBox>
          <CardBoxComponentEmpty />
        </CardBox>
      )}
      {props.users.length > 1 && (
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

export default TableUsers
