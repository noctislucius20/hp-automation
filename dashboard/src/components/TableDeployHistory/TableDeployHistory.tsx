import BaseButton from '../BaseButton'
import BaseButtons from '../BaseButtons'
import CardBox from '../CardBox'
import CardBoxComponentEmpty from '../CardBoxComponentEmpty'

interface DeployHistory {
  ip_address: string
  name: string
  job_history: {
    deployment_status: string
    finished_at: string
  }
}

type Props = {
  deployHistory: DeployHistory[]
  status: object
  currentPage: number
  pageChange: (page: number) => void
}

const TableDeployHistory = (props: Props) => {
  const perPage = 5
  const deployHistoryPaginated = props.deployHistory.slice(
    perPage * props.currentPage,
    perPage * (props.currentPage + 1)
  )
  const numPages = Math.ceil(props.deployHistory.length / perPage)
  const pagesList = []

  for (let i = 0; i < numPages; i++) {
    pagesList.push(i)
  }

  const handleStatusDeploymentColor = (deploymentStatus) => {
    let statusColor = ''
    switch (deploymentStatus) {
      case 'failed':
        statusColor = 'text-red-700'
        break
      case 'canceled':
        statusColor = 'text-yellow-700'
        break
      case 'successful':
        statusColor = 'text-green-700'
        break
      case 'error':
        statusColor = 'text-red-700'
        break
      default:
        statusColor = 'text-blue-700'
    }
    return statusColor
  }

  return (
    <>
      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Name</th>
            <th>Deployment Status</th>
            <th>Finished</th>
          </tr>
        </thead>
        <tbody>
          {deployHistoryPaginated.map((deployHistory, index) => (
            <>
              <tr key={index}>
                <td data-label="IP Address">{deployHistory.ip_address}</td>
                <td data-label="Name">{deployHistory.name}</td>
                <td data-label="Deployment Status">
                  <span
                    className={handleStatusDeploymentColor(
                      deployHistory.job_history.deployment_status
                    )}
                  >
                    {deployHistory.job_history.deployment_status.charAt(0).toUpperCase() +
                      deployHistory.job_history.deployment_status.slice(1)}
                  </span>
                </td>
                <td data-label="Finished">
                  {deployHistory.job_history.finished_at
                    ? new Date(deployHistory.job_history.finished_at).toLocaleString()
                    : '-'}
                </td>
              </tr>
            </>
          ))}
        </tbody>
      </table>
      {props.deployHistory.length === 0 && (
        <CardBox>
          <CardBoxComponentEmpty />
        </CardBox>
      )}
      {props.deployHistory.length > 0 && (
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

export default TableDeployHistory
