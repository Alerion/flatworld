var gulp = require('gulp');
var less = require('gulp-less');
var sourcemaps = require('gulp-sourcemaps');
var del = require('del');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var browserify = require('browserify');
var watchify = require('watchify');
var babelify = require('babelify');
var bower = require('gulp-bower');
var path = require('path');
var NpmImportPlugin = require("less-plugin-npm-import");

function compile(watch) {
    var bundler =
        browserify('./app/js/index.js', { debug: true })
        .transform(
            babelify.configure({
                optional: ["runtime", "es7.asyncFunctions"]
            })
          );

    bundller =  watch ? watchify(bundler) : bundler;

    function rebundle() {
        bundler.bundle()
            .on('error', function(err) { console.error(err); this.emit('end'); })
            .pipe(source('build.js'))
            .pipe(buffer())
            .pipe(sourcemaps.init({ loadMaps: true }))
            .pipe(sourcemaps.write('./'))
            .pipe(gulp.dest('./build/js'));
    }

    if (watch) {
        bundler.on('update', function() {
            console.log('-> bundling...');
            rebundle();
        });
    }

    rebundle();
}

gulp.task('cssbuild', function () {
    return gulp.src('./app/less/app.less')
        .pipe(sourcemaps.init())
        .pipe(less({
            plugins: [new NpmImportPlugin({prefix: 'npm://'})]
        }))
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./build/css'));
});

gulp.task('csswatch', function () {
    return gulp.watch('./app/less/**/*.less', ['cssbuild', 'fontsbuild']);
});

gulp.task('jswatch', function() {
    return compile(true);
});

gulp.task('jsbuild', function() {
    return compile();
});

gulp.task('fontsbuild', function() {
    return gulp.src([
            './app/fonts/**/*.{ttf,woff,woff2,eof,svg}'
        ])
        .pipe(gulp.dest('./build/fonts'));
});

gulp.task('imgbuild', function() {
    return gulp.src('./app/img/**/*.{png,gif,jpg}')
        .pipe(gulp.dest('./build/img'));
});

gulp.task('clean', function (cb) {
    del(['build'], cb)
});

gulp.task('bower', function() {
    return bower()
        .pipe(gulp.dest('./build/vendors'))
});

gulp.task('build', ['bower', 'jsbuild', 'cssbuild', 'fontsbuild', 'imgbuild']);
gulp.task('watch', ['jswatch', 'csswatch']);

gulp.task('default', ['watch']);
