/*jshint esversion: 6 */
import Axios from '@/utils/axios.js';

//获取MongodbInst信息
export const getMongodbInstList = () => { return Axios.oGet(`/mongodbinst/`) }