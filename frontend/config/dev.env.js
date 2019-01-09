'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

const baseUrl = '"http://journey.api:8888/api"'

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  baseUrl: baseUrl
})
