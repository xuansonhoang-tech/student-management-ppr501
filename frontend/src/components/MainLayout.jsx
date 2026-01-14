import React from 'react';

const MainLayout = ({ children }) => {
  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      flexDirection: 'column', 
      fontFamily: "'Segoe UI', Roboto, sans-serif",
      backgroundColor: '#f5f6fa'
    }}>
      
      {/* HEADER: Siêu tối giản, chỉ còn Logo */}
      <header style={{ 
        backgroundColor: '#2c3e50', 
        color: 'white', 
        padding: '0 20px', 
        height: '60px', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', // Căn giữa chữ UniManager
        boxShadow: '0 2px 5px rgba(0,0,0,0.1)' 
      }}>
        <div style={{ fontSize: '20px', fontWeight: 'bold' }}>GROUP_4</div>
      </header>

      {/* BODY: Chứa nội dung trang web */}
      <main style={{ 
        flex: 1, 
        width: '100%', 
        maxWidth: '1200px', 
        margin: '0 auto', 
        padding: '20px' 
      }}>
        {children}
      </main>

      {/* FOOTER: Đã đổi thành Group 4 */}
      <footer style={{ 
        textAlign: 'center', 
        padding: '15px', 
        color: '#7f8c8d', 
        fontSize: '13px', 
        borderTop: '1px solid #dcdcdc', 
        backgroundColor: 'white' 
      }}>
        Group 4
      </footer>

    </div>
  );
};

export default MainLayout;