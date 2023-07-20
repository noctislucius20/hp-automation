import BaseButton from '../BaseButton'
import BaseButtons from '../BaseButtons'
import CardBox from '../CardBox'
import CardBoxComponentEmpty from '../CardBoxComponentEmpty'

interface JobHistory {
  deployment_status: string
  finished_at: string
}

type Props = {
  jobHistory: JobHistory[]
  status: object
  currentPage: number
  pageChange: (page: number) => void
}

const TableJobHistory = (props: Props) => {
  const perPage = 5
  const jobHistoryPaginated = props.jobHistory.slice(
    perPage * props.currentPage,
    perPage * (props.currentPage + 1)
  )
  const numPages = Math.ceil(props.jobHistory.length / perPage)
  const pagesList = []

  for (let i = 0; i < numPages; i++) {
    pagesList.push(i)
  }

  const handleStatusJobColor = (jobStatus) => {
    let statusColor = ''
    switch (jobStatus) {
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
            <th>Finished</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {jobHistoryPaginated.map((jobHistory, index) => (
            <tr key={index}>
              <td data-label="Finished">
                {jobHistory.finished_at ? new Date(jobHistory.finished_at).toLocaleString() : '-'}
              </td>
              <td data-label="Status">
                <span className={handleStatusJobColor(jobHistory.deployment_status)}>
                  {jobHistory.deployment_status.charAt(0).toUpperCase() +
                    jobHistory.deployment_status.slice(1)}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {props.jobHistory.length === 0 && (
        <CardBox>
          <CardBoxComponentEmpty />
        </CardBox>
      )}

      {props.jobHistory.length > 0 && (
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

export default TableJobHistory
