/*jshint esversion: 6 */
import request from '../utils/request.js';

export const ShowCharts = params => { return request.post('/showcharts',params) };