var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');

var input = ['scss/styles.scss'];
var output = 'static';

function css() {
    gulp.watch(input, function(cb) {
        return gulp.src(input)
        .pipe(sass())
        .pipe(gulp.dest(output))
      });
}

function build() {
    return gulp.src(input)
    .pipe(sass())
    .pipe(gulp.dest(output))
}

exports.css = css;
exports.build = build;
exports.default = gulp.parallel(css);