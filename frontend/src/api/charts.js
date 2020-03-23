/*jshint esversion: 6 */
import request from '../utils/request.js';

export const ShowCharts = () => { return request.get('/showcharts/') };