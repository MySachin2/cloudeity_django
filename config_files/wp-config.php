<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //

define('DB_CHARSET', 'utf8');

define('DB_COLLATE', '');


define('DB_NAME', 'wordpress');
define('DB_USER', 'wordpressuser');
define('DB_PASSWORD', 'wordpress');
define('DB_HOST', 'localhost');
define('AUTH_KEY',         '|Sg xn _BNqhS LqqvjHQD,>`at}8i+G+U;2VJ*5K&KuO~=N0(sS<9N~EJ,aGzN*');
define('SECURE_AUTH_KEY',  'r7Mq4~Shq>5GRs3)1K,9W<5Nm;dX2BY):Q<i)FHC2<E:CU>|A~ab{39{y>`/FuiI');
define('LOGGED_IN_KEY',    '1I!t-;@7,Gamh}-;VeHm1LxV=U$LVAJjT%H7&`Qd{<J&N14GoyBVIcFy!0{jg&PI');
define('NONCE_KEY',        ':~dQrg7Xuyd^Wr873k$]du+4L*Lt//j[dT}60aP+7vg9T#F x{|,GGQa-|p{P;PP');
define('AUTH_SALT',        '?Ii@6|s&&@NWI-~1;gF?BMMe&wXdl}a9M^W/)(-6*%A,mT~QRocK`O)?MAx)2Frd');
define('SECURE_AUTH_SALT', '=%EMR]Ij>#gzy=Xt|{4`cz~VgdP`o/}qAhWla*]C/Z`3Mej,?7-d+xF-37O:ELLu');
define('LOGGED_IN_SALT',   'HgEnpJk)-%^MrgH$BYbF)cIoYrj|,&iXf_0h%]>P^2%7UY:G6$G9=lKt)e?mCky!');
define('NONCE_SALT',       'Qe/cVb{F>:wwD/MIqVUCL9v+rT2=]L*iDIF 6HiC9 n@rxPRec-al5R19GQqSkcV');

define('FS_METHOD', 'direct');
define('FORCE_SSL', true);
define('FORCE_SSL_ADMIN',true);
/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
