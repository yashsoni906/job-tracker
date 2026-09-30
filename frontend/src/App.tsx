import { useQuery } from '@tanstack/react-query';
import { apiClient } from './api/client';
import type { Application } from './types';

function App() {
  const { data: applications, isLoading, error } = useQuery<Application[]>({
    queryKey: ['applications'],
    queryFn: async () => {
      const response = await apiClient.get('/applications/');
      return response.data;
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading applications</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Job Applications</h1>
      <ul>
        {applications?.map((app) => (
          <li key={app.id}>
            {app.role_title} — {app.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;