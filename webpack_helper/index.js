var fs = require('fs');

/* load configuration from django */
var django_config_path = process.env.DJANGO_WEBPACK_CONFIG;
if (django_config_path === undefined || django_config_path === null) {
    throw new Error('DJANGO_WEBPACK_CONFIG environment variable must be set to a valid json file.');
}

var django = JSON.parse(fs.readFileSync(django_config_path, 'utf8'));

var MODULE_DIRECTORIES = django.WEBPACK_EXTRA_MODULE_DIRECTORIES;
Array.prototype.push.apply(MODULE_DIRECTORIES, ['node_modules', 'bower_components']);
django.MODULE_DIRECTORIES = MODULE_DIRECTORIES;

module.exports = django;
