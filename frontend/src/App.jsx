import React from 'react';
import StudentPage from './pages/StudentPage';
import MainLayout from './components/MainLayout'; // Import file vừa tạo

function App() {
  return (
    // Bọc toàn bộ ứng dụng trong MainLayout
    <MainLayout>
      <StudentPage />
    </MainLayout>
  );
}

export default App;