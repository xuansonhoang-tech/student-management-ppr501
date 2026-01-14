import React, { useState, useEffect } from 'react';
import axios from 'axios';
// Thư viện vẽ biểu đồ (Dùng cho tính năng Thống kê điểm số)
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

/**
 * STYLE CONFIGURATION
 * Định nghĩa CSS-in-JS để đảm bảo tính nhất quán của giao diện.
 * Sử dụng MainLayout làm khung, component này chỉ lo phần nội dung.
 */
const styles = {
    container: { padding: '0', color: '#333' },
    
    // Header & Layout components
    header: { fontSize: '24px', fontWeight: '700', marginBottom: '25px', color: '#2c3e50', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eee', paddingBottom: '15px' },
    card: { backgroundColor: 'white', borderRadius: '6px', border: '1px solid #e0e0e0', padding: '20px', marginBottom: '20px' },
    toolbar: { display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '15px' },
    
    // Form Elements
    input: { padding: '8px 12px', borderRadius: '4px', border: '1px solid #ced4da', fontSize: '14px', outline: 'none', transition: 'border-color 0.2s' },
    formGroup: { marginBottom: '15px' },
    label: { display: 'block', marginBottom: '6px', fontWeight: '600', fontSize: '13px', color: '#495057' },
    formInput: { width: '100%', padding: '8px', border: '1px solid #ced4da', borderRadius: '4px', boxSizing: 'border-box' },

    // Buttons (Phân loại theo chức năng: Primary, Secondary, Danger)
    btnPrimary: { padding: '8px 16px', backgroundColor: '#0d6efd', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: '500', fontSize: '14px' },
    btnSecondary: { padding: '8px 16px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '14px' },
    btnStats: { padding: '8px 16px', backgroundColor: '#6610f2', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: '500', fontSize: '14px' },
    btnToggle: { padding: '8px 16px', backgroundColor: '#198754', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: '500', fontSize: '14px' },
    btnEdit: { padding: '5px 10px', backgroundColor: '#ffc107', color: '#212529', border: '1px solid #ffc107', borderRadius: '3px', cursor: 'pointer', fontSize: '12px', fontWeight: '500' },
    btnDanger: { padding: '5px 10px', backgroundColor: '#dc3545', color: 'white', border: '1px solid #dc3545', borderRadius: '3px', cursor: 'pointer', fontSize: '12px', fontWeight: '500', marginLeft: '5px' },

    // Table Styling
    tableContainer: { overflowX: 'auto', border: '1px solid #dee2e6', borderRadius: '4px' },
    table: { width: '100%', borderCollapse: 'collapse', fontSize: '14px', backgroundColor: 'white' },
    th: { padding: '12px 15px', fontWeight: '600', color: '#495057', textAlign: 'left', borderBottom: '2px solid #dee2e6', backgroundColor: '#f8f9fa' },
    td: { padding: '12px 15px', borderBottom: '1px solid #dee2e6', color: '#212529' },
    tdCenter: { padding: '12px 15px', borderBottom: '1px solid #dee2e6', textAlign: 'center', color: '#212529' },

    // Modal Components
    modalOverlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1050 },
    modalContent: { backgroundColor: 'white', padding: '30px', borderRadius: '8px', width: '700px', maxWidth: '95%', boxShadow: '0 5px 15px rgba(0,0,0,0.3)', maxHeight: '90vh', overflowY: 'auto' },
    statBox: { flex: 1, padding: '15px', backgroundColor: '#f8f9fa', border: '1px solid #dee2e6', borderRadius: '4px', textAlign: 'center' },
    statValue: { fontSize: '18px', fontWeight: 'bold', color: '#212529', marginTop: '5px' },
    statLabel: { fontSize: '12px', color: '#6c757d', textTransform: 'uppercase', letterSpacing: '0.5px' },
};

const StudentPage = () => {
  // --- STATE MANAGEMENT ---
  // Dữ liệu danh sách sinh viên và phân trang
  const [students, setStudents] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);

  // Trạng thái giao diện (View Mode vs Manage Mode)
  const [isEditMode, setIsEditMode] = useState(false); 
  
  // Trạng thái Analytics (Thống kê)
  const [isStatsOpen, setIsStatsOpen] = useState(false);
  const [statsData, setStatsData] = useState([]);
  const [statsSummary, setStatsSummary] = useState(null);

  // Bộ lọc & Tìm kiếm (Filter Params)
  const [keyword, setKeyword] = useState("");
  const [filterField, setFilterField] = useState("first_name"); // Mặc định tìm theo tên
  const [sortBy, setSortBy] = useState("student_id");           // Mặc định sắp xếp theo ID
  const [order, setOrder] = useState("asc");                    // Mặc định tăng dần

  // Trạng thái Modal CRUD (Thêm/Sửa)
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false); // true: Edit Mode, false: Create Mode
  const [formData, setFormData] = useState({
    student_id: "", first_name: "", last_name: "", email: "", 
    hometown: "", dob: "", math_score: 0, literature_score: 0, english_score: 0
  });

  // --- API SERVICE FUNCTIONS ---

  /**
   * Lấy danh sách sinh viên từ Backend với các tham số lọc/phân trang.
   * Endpoint: GET /students/list
   */
  const fetchStudents = async (currentPage) => {
    setLoading(true);
    try {
      // Mapping tham số Frontend sang chuẩn Backend yêu cầu
      const params = { page: currentPage, page_size: 10 };
      
      // Chỉ gửi filter khi có từ khóa
      if (keyword.trim()) { 
          params.filter_field = filterField; 
          params.filter_value = keyword; 
      }
      
      // Mapping sort param
      if (sortBy) { 
          params.sort_field = sortBy; 
          params.ascending = order === 'asc'; // Backend nhận boolean (True/False)
      }

      const response = await axios.get(`http://127.0.0.1:8000/students/list`, { params });
      
      if (response.data && response.data.data) {
        setStudents(response.data.data);
        const total = response.data.total || 100;
        setTotalPages(Math.ceil(total / 10)); // Giả định page_size = 10
      } else { 
        setStudents([]); 
      }
    } catch (error) { 
        console.error("Lỗi khi gọi API danh sách sinh viên:", error); 
        setStudents([]); 
    } finally { 
        setLoading(false); 
    }
  };

  /**
   * Lấy dữ liệu thống kê điểm số.
   * Endpoint: GET /students/analysis/points
   * Xử lý: Chuyển đổi dữ liệu JSON từ BE sang format mảng cho Recharts.
   */
  const fetchStats = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/students/analysis/points`);
      
      if (response.data && response.data.data && response.data.data.length > 0) {
        const raw = response.data.data[0];
        // Fallback object phòng trường hợp BE chưa trả về môn Literature
        const lit = raw.literature || { excellent_percentage: 0, average_percentage: 0, poor_percentage: 0, max_point: 0, min_point: 0 };
        
        // Transform data cho biểu đồ (BarChart)
        const chartData = [
            { name: "Excellent", Math: parseFloat(raw.math.excellent_percentage.toFixed(1)), Literature: parseFloat(lit.excellent_percentage.toFixed(1)), English: parseFloat(raw.english.excellent_percentage.toFixed(1)) },
            { name: "Average", Math: parseFloat(raw.math.average_percentage.toFixed(1)), Literature: parseFloat(lit.average_percentage.toFixed(1)), English: parseFloat(raw.english.average_percentage.toFixed(1)) },
            { name: "Poor", Math: parseFloat(raw.math.poor_percentage.toFixed(1)), Literature: parseFloat(lit.poor_percentage.toFixed(1)), English: parseFloat(raw.english.poor_percentage.toFixed(1)) }
        ];
        
        setStatsData(chartData);
        setStatsSummary({
            math: { max: raw.math.max_point, min: raw.math.min_point },
            literature: { max: lit.max_point, min: lit.min_point },
            english: { max: raw.english.max_point, min: raw.english.min_point }
        });
        
        setIsStatsOpen(true);
      } else { 
          alert("Dữ liệu thống kê trống hoặc lỗi cấu trúc API."); 
      }
    } catch (error) { 
        console.error("Lỗi API Analytics:", error);
        alert("Không thể tải dữ liệu thống kê. Vui lòng kiểm tra Backend.");
    }
  };

  // Tự động gọi API khi component mount hoặc page thay đổi
  useEffect(() => { fetchStudents(page); }, [page]);

  // --- CRUD HANDLERS ---

  const handleDelete = async (studentId) => { 
    // Yêu cầu xác nhận trước khi xóa (Client-side validation)
    if (window.confirm(`Are you sure you want to delete student ID: ${studentId}?`)) { 
        try { 
            await axios.delete(`http://127.0.0.1:8000/students/${studentId}`); 
            fetchStudents(page); // Reload danh sách sau khi xóa
        } catch (error) { 
            alert("Delete failed! Please check console."); 
        } 
    } 
  };

  // Reset form về trạng thái Create
  const handleOpenCreate = () => { 
      setFormData({ student_id: "", first_name: "", last_name: "", email: "", hometown: "", dob: "2003-01-01", math_score: 0, literature_score: 0, english_score: 0 }); 
      setIsEditing(false); 
      setIsModalOpen(true); 
  };

  // Fill dữ liệu vào form để Edit
  const handleOpenEdit = (student) => { 
      setFormData({ ...student }); 
      setIsEditing(true); 
      setIsModalOpen(true); 
  };

  // Xử lý Submit Form (Dùng chung cho cả Create và Update)
  const handleSubmit = async (e) => { 
      e.preventDefault(); // Ngăn reload trang
      try { 
          if (isEditing) {
              // Endpoint: PATCH /students/ (Cập nhật)
              await axios.patch(`http://127.0.0.1:8000/students/`, formData); 
          } else {
              // Endpoint: POST /students/ (Tạo mới)
              await axios.post(`http://127.0.0.1:8000/students/`, formData); 
          }
          setIsModalOpen(false); 
          fetchStudents(page); // Refresh dữ liệu
      } catch (error) { 
          alert("Action failed. Please check for duplicate IDs or invalid data."); 
      } 
  };

  // --- RENDER COMPONENT ---
  return (
    <div style={styles.container}>
      {/* HEADER SECTION */}
      <div style={styles.header}>
        <span>Student Management</span>
        <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={fetchStats} style={styles.btnStats}>
                View Analytics
            </button>
            <button onClick={() => setIsEditMode(!isEditMode)} style={styles.btnToggle}>
                {isEditMode ? "Switch to View Mode" : "Switch to Manage Mode"}
            </button>
            {isEditMode && (
                <button onClick={handleOpenCreate} style={styles.btnPrimary}>
                    Add New Student
                </button>
            )}
        </div>
      </div>

      {/* FILTER & SORT TOOLBAR */}
      <div style={styles.card}>
        <div style={styles.toolbar}>
            <div style={{ display: 'flex', gap: '10px' }}>
                <select value={filterField} onChange={(e) => setFilterField(e.target.value)} style={styles.input}>
                    <option value="first_name">Filter by Name</option>
                    <option value="student_id">Filter by ID</option>
                    <option value="hometown">Filter by Hometown</option>
                </select>
                <input 
                    type="text" 
                    placeholder="Enter keyword..." 
                    value={keyword} 
                    onChange={(e) => setKeyword(e.target.value)} 
                    style={{ ...styles.input, width: '250px' }} 
                />
                <button onClick={() => { setPage(1); fetchStudents(1); }} style={styles.btnPrimary}>
                    Search
                </button>
            </div>
            
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} style={styles.input}>
                    <option value="student_id">Sort by ID</option>
                    <option value="math_score">Sort by Math</option>
                </select>
                <select value={order} onChange={(e) => setOrder(e.target.value)} style={styles.input}>
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
                </select>
                <button onClick={() => { setPage(1); fetchStudents(1); }} style={styles.btnSecondary}>
                    Apply
                </button>
            </div>
        </div>
      </div>

      {/* DATA TABLE SECTION */}
      <div style={styles.card}>
        <div style={styles.tableContainer}>
            <table style={styles.table}>
            <thead>
                <tr>
                    <th style={styles.tdCenter}>ID</th>
                    <th style={styles.th}>Full Name</th>
                    <th style={styles.th}>Email</th>
                    <th style={styles.th}>Hometown</th>
                    <th style={styles.tdCenter}>Math</th>
                    <th style={styles.tdCenter}>Literature</th>
                    <th style={styles.tdCenter}>English</th>
                    {/* Chỉ hiện cột Actions khi ở chế độ Manage */}
                    {isEditMode && <th style={{ ...styles.th, textAlign: 'center', width: '150px' }}>Actions</th>}
                </tr>
            </thead>
            <tbody>
                {loading ? (
                    <tr><td colSpan="8" style={{ padding: '40px', textAlign: 'center', color: '#6c757d' }}>Loading data...</td></tr>
                ) : (
                    students.map((st, idx) => (
                    <tr key={st.student_id} style={{ backgroundColor: idx % 2 === 0 ? 'white' : '#f8f9fa' }}>
                        <td style={styles.tdCenter}>{st.student_id}</td>
                        <td style={styles.td}>{st.last_name} {st.first_name}</td>
                        <td style={styles.td}>{st.email}</td>
                        <td style={styles.td}>{st.hometown}</td>
                        <td style={styles.tdCenter}>{st.math_score}</td>
                        <td style={styles.tdCenter}>{st.literature_score}</td>
                        <td style={styles.tdCenter}>{st.english_score}</td>
                        {isEditMode && (
                            <td style={{ ...styles.td, textAlign: 'center' }}>
                                <button onClick={() => handleOpenEdit(st)} style={styles.btnEdit}>Edit</button>
                                <button onClick={() => handleDelete(st.student_id)} style={styles.btnDanger}>Delete</button>
                            </td>
                        )}
                    </tr>
                    ))
                )}
            </tbody>
            </table>
        </div>
        
        {/* PAGINATION */}
        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end', gap: '10px', alignItems: 'center' }}>
            <button onClick={() => setPage(Math.max(page - 1, 1))} disabled={page === 1} style={styles.btnSecondary}>Previous</button>
            <span style={{ fontSize: '14px', color: '#6c757d' }}>Page {page} of {totalPages}</span>
            <button onClick={() => setPage(Math.min(page + 1, totalPages))} disabled={page === totalPages} style={styles.btnSecondary}>Next</button>
        </div>
      </div>

      {/* ANALYTICS MODAL */}
      {isStatsOpen && (
        <div style={styles.modalOverlay} onClick={() => setIsStatsOpen(false)}>
            <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
                <div style={{display:'flex', justifyContent: 'space-between', alignItems:'center', marginBottom: '20px', borderBottom: '1px solid #eee', paddingBottom: '15px'}}>
                    <h3 style={{margin:0, color: '#212529'}}>Performance Analysis</h3>
                    <button onClick={() => setIsStatsOpen(false)} style={{border:'none', background:'transparent', fontSize:'24px', cursor:'pointer', color:'#adb5bd'}}>×</button>
                </div>
                
                <h4 style={{textAlign:'center', color:'#495057', marginBottom: '20px'}}>Score Distribution (%)</h4>
                <div style={{ width: '100%', height: 350 }}>
                    <ResponsiveContainer>
                        <BarChart data={statsData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e9ecef" />
                            <XAxis dataKey="name" axisLine={false} tickLine={false} />
                            <YAxis axisLine={false} tickLine={false} unit="%" />
                            <Tooltip cursor={{fill: '#f8f9fa'}} contentStyle={{borderRadius: '8px', border: '1px solid #dee2e6'}} />
                            <Legend />
                            <Bar dataKey="Math" fill="#0d6efd" radius={[4, 4, 0, 0]} name="Math" />
                            <Bar dataKey="Literature" fill="#fd7e14" radius={[4, 4, 0, 0]} name="Literature" />
                            <Bar dataKey="English" fill="#20c997" radius={[4, 4, 0, 0]} name="English" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Score Summary Cards */}
                {statsSummary && (
                    <div style={{display: 'flex', gap: '15px', marginTop: '25px'}}>
                        <div style={styles.statBox}>
                            <div style={styles.statLabel}>Math (Max/Min)</div>
                            <div style={styles.statValue}>{statsSummary.math.max} / {statsSummary.math.min}</div>
                        </div>
                        <div style={styles.statBox}>
                            <div style={styles.statLabel}>Literature (Max/Min)</div>
                            <div style={styles.statValue}>{statsSummary.literature.max} / {statsSummary.literature.min}</div>
                        </div>
                        <div style={styles.statBox}>
                            <div style={styles.statLabel}>English (Max/Min)</div>
                            <div style={styles.statValue}>{statsSummary.english.max} / {statsSummary.english.min}</div>
                        </div>
                    </div>
                )}
            </div>
        </div>
      )}

      {/* CRUD MODAL (CREATE / EDIT) */}
      {isModalOpen && (
        <div style={styles.modalOverlay}>
          <div style={{...styles.modalContent, width: '600px'}}>
            <h3 style={{ marginTop: 0, marginBottom: '20px', color: '#212529' }}>
                {isEditing ? "Edit Student Information" : "Create New Student"}
            </h3>
            <form onSubmit={handleSubmit}>
              {/* Row 1: ID & DOB */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Student ID</label>
                    <input required disabled={isEditing} style={styles.formInput} value={formData.student_id} onChange={(e) => setFormData({...formData, student_id: e.target.value})} />
                </div>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Date of Birth</label>
                    <input type="date" required style={styles.formInput} value={formData.dob} onChange={(e) => setFormData({...formData, dob: e.target.value})} />
                </div>
              </div>
              
              {/* Row 2: Name */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                <div style={styles.formGroup}>
                    <label style={styles.label}>First Name</label>
                    <input required style={styles.formInput} value={formData.first_name} onChange={(e) => setFormData({...formData, first_name: e.target.value})} />
                </div>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Last Name</label>
                    <input required style={styles.formInput} value={formData.last_name} onChange={(e) => setFormData({...formData, last_name: e.target.value})} />
                </div>
              </div>

              {/* Row 3: Contact */}
              <div style={styles.formGroup}>
                  <label style={styles.label}>Email Address</label>
                  <input type="email" required style={styles.formInput} value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} />
              </div>
              <div style={styles.formGroup}>
                  <label style={styles.label}>Hometown</label>
                  <input required style={styles.formInput} value={formData.hometown} onChange={(e) => setFormData({...formData, hometown: e.target.value})} />
              </div>

              {/* Row 4: Scores */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px' }}>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Math</label>
                    <input type="number" step="0.1" style={styles.formInput} value={formData.math_score} onChange={(e) => setFormData({...formData, math_score: Number(e.target.value)})} />
                </div>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Literature</label>
                    <input type="number" step="0.1" style={styles.formInput} value={formData.literature_score} onChange={(e) => setFormData({...formData, literature_score: Number(e.target.value)})} />
                </div>
                <div style={styles.formGroup}>
                    <label style={styles.label}>English</label>
                    <input type="number" step="0.1" style={styles.formInput} value={formData.english_score} onChange={(e) => setFormData({...formData, english_score: Number(e.target.value)})} />
                </div>
              </div>

              {/* Form Actions */}
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '25px', borderTop: '1px solid #eee', paddingTop: '15px' }}>
                <button type="button" onClick={() => setIsModalOpen(false)} style={styles.btnSecondary}>Cancel</button>
                <button type="submit" style={styles.btnPrimary}>Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentPage;