import { useState } from 'react'
import axios from 'axios'
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// Configure axios defaults
const api = axios.create({
  // baseURL: 'http://127.0.0.1:8000 ',
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

interface Job {
  company: string,
  title: string,
  info: string
}

function App() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const startScraping = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await api.post('/scrape')
      console.log('Scrape initiated:', response.data);
      await pollResults()
    } catch (error: any) {
      console.error('Error details:', {
        message: error.message,
        response: error.response,
        request: error.request
      });
      const errorMessage = error.response 
        ? `Error ${error.response.status}: ${error.response.statusText}`
        : 'Network error - Is the backend server running?';
      setError(errorMessage)
      setIsLoading(false)
    }
  }

  const pollResults = async (attempts = 0, maxAttempts = 30) => {
    if (attempts >= maxAttempts) {
      setError('Timed out waiting for results')
      setIsLoading(false)
      return
    }

    try {
      const response = await api.get('/results')
      console.log('Poll response:', response.data);
      if (response.data.data && response.data.data.length > 0) {
        setJobs(response.data.data)
        setIsLoading(false)
      } else {
        setTimeout(() => pollResults(attempts + 1), 2000)
      }
    } catch (error: any) {
      console.error('Poll error details:', {
        message: error.message,
        response: error.response,
        request: error.request
      });
      const errorMessage = error.response 
        ? `Error ${error.response.status}: ${error.response.statusText}`
        : 'Network error - Is the backend server running?';
      setError(errorMessage)
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Company Search Results</h1>
      <Button onClick={startScraping} disabled={isLoading}>
        {isLoading ? 'Searching Companies...' : 'Start Company Search'}
      </Button>

      {error && (
        <div className="text-red-500 mt-4">
          <p>Error: {error}</p>
          <p className="text-sm mt-1">Make sure the backend server is running on http://localhost:8000</p>
        </div>
      )}

      {jobs.length > 0 && (
        <div className="mt-4">
          <p className="text-gray-600 mb-2">Found {jobs.length} job listings</p>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Company</TableHead>
                <TableHead>Title</TableHead>
                <TableHead>Additional Info</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {jobs.map((job, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{job.company}</TableCell>
                  <TableCell>{job.title}</TableCell>
                  <TableCell className="text-gray-600">{job.info}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}

export default App