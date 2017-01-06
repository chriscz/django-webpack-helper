var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var django = require('django-webpack-helper');

module.exports = {
  context: __dirname,

  debug: true,

  entry: {
       /* 
        * NOTE: Django Webpack Helper 
        * List the calculated absolute paths to all your apps entries here.
        * All entry points should use a unique prefix (your django app label)
        * To prevent conflicts in the future.
        *
        * Below is an example entry
        *
        * 'appname-index': [ path.join(__dirname, '/assets/index/app.js') ],
        */

  }, 

  /* READ AS: for each e in entry, apply `output` */
  output: {
      path: django.WEBPACK_BUNDLE_DIR,
      filename: "[name]-[hash].js",
      /* NOTE: used to expose your assets */
      publicPath: django.WEBPACK_PUBLIC_PATH,
  },

  plugins: [
    /* NOTE the output of this plugin will be used by django */
    new BundleTracker({
            path: path.dirname(django.WEBPACK_STATS_FILE), 
            filename: path.basename(django.WEBPACK_STATS_FILE) 
    }),
  ],

  module: {
    /* NOTE these loaders are always applied to the filetypes that they match */
    loaders: [
        /* look at
         *   - https://github.com/jtangelder/sass-loader for sass loading
         *   - http://stackoverflow.com/a/32223731
         * the following snippet was taken from
         *   - https://github.com/AngularClass/angular2-webpack-starter/issues/696#issuecomment-227786637
         *     for including bootstrap and jquery
         */
    ],
  },

  resolveLoader: {
    modulesDirectories: django.MODULE_DIRECTORIES,
  },
  resolve: {
    extensions: ['', '.js', '.css', '.scss', '.less'],
    modulesDirectories: django.MODULE_DIRECTORIES
  },
}

