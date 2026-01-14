// src/utils/api.js
import axios from 'axios';
import { API_BASE_URL } from './constants';

const api = axios.create({
    baseURL: API_BASE_URL,
});

// PHẢI CÓ từ khóa 'export' và tên hàm là 'fetchStudents'
export const fetchStudents = (page = 1, pageSize = 10) => {
    return api.get(`/students/list`, {
        params: {
            page: page,
            page_size: pageSize
        }
    });
};