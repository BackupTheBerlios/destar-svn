/*
 * Asterisk -- A telephony toolkit for Linux.
 *
 * SQlite Database access functions
 *
 * Copyright <c> 2004 Michael Bielicki <Michael.Bielicki@taansoftworks.com>
 *
 * This program is free software, distributed under the terms of
 * the GNU General Public License
 *
 * Based on work by Holger Scheurig - cdr_sqlite.c
 *  Based on work by Brian K. West - app_dbodbc.c
 * Based on work by Mark Spencer and Jefferson Noxon - app_db.c
 *
 */

#include <sys/types.h>
#include <asterisk/options.h>
#include <asterisk/config.h>
#include <asterisk/file.h>
#include <asterisk/logger.h>
#include <asterisk/channel.h>
#include <asterisk/pbx.h>
#include <asterisk/module.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include "../asterisk.h"
#include "../astconf.h"
#include <sqlite.h>

static char *tdesc = "SQlite Database access functions for Asterisk extension logic";

static char *g_descrip =
  "  SQliteget(varname=family/key): Retrieves a value from the Asterisk\n"
  "database and stores it in the given variable.  Always returns 0.  If the\n"
  "requested key is not found, jumps to priority n+101 if available.\n";

static char *p_descrip =
  "  SQliteput(family/key=value): Stores the given value in the Asterisk\n"
  "database.  Always returns 0.\n";

static char *d_descrip =
  "  SQlitedel(family/key): Deletes a key from the Asterisk database.  Always\n"
  "returns 0.\n";

static char *dt_descrip =
  "  SQlitedeltree(family[/keytree]): Deletes a family or keytree from the Asterisk\n"
  "database.  Always returns 0.\n";

static char *g_app = "SQliteget";
static char *p_app = "SQliteput";
static char *d_app = "SQlitedel";
static char *dt_app = "SQlitedeltree";

static char *g_synopsis = "Retrieve a value from a SQlite datasource";
static char *p_synopsis = "Store a value in a SQlite datasource";
static char *d_synopsis = "Delete a key from a SQlite datasource";
static char *dt_synopsis = "Delete a family or keytree from a SQlite datasource";

static sqlite* db = NULL;

AST_MUTEX_DEFINE_STATIC(sqlite_lock);

static char sql_create_table[] = "CREATE TABLE astdb ("
"       Id          INTEGER PRIMARY KEY,"
"       astfamily            VARCHAR(80),"
"       astkey             VARCHAR(80),"
"       astvalue             VARCHAR(80)"
");";

static int connected = 0;

static int ast_db_sqliteget(char *family, char *key, char *out, int outlen);
static int ast_db_sqliteput(char *family, char *key, char *value);
static int ast_db_sqlitedel(char *family, char *key);
static int ast_db_sqlitedeltree(char *family, char *keytree);
static int sqlite_load_module(void);
static int sqlite_unload_module(void);

STANDARD_LOCAL_USER;

LOCAL_USER_DECL;

static int sqlitedeltree_exec(struct ast_channel *chan, void *data)
{
	int arglen;
	char *argv, *family, *keytree;

	arglen = strlen (data);
	argv = alloca (arglen + 1);
	if (!argv)			/* Why would this fail? */
	{
		ast_log (LOG_DEBUG, "Memory allocation failed\n");
		return 0;
	}

	memcpy (argv, data, arglen + 1);

	if (strchr (argv, '/'))
	{
		family = strsep (&argv, "/");
		keytree = strsep (&argv, "\0");
		if (!family || !keytree)
		{
			ast_log (LOG_DEBUG, "Ignoring; Syntax error in argument\n");
			return 0;
		}
		if (!strlen (keytree))
			keytree = 0;
  	}
	else
	{
		family = argv;
		keytree = 0;
	}

	if (option_verbose > 2)
	{
		if (keytree)
			ast_verbose (VERBOSE_PREFIX_3 "sqlitedeltree: family=%s, keytree=%s\n", family, keytree);
    		else
      			ast_verbose (VERBOSE_PREFIX_3 "sqlitedeltree: family=%s\n", family);
	}

	if (ast_db_sqlitedeltree (family, keytree))
	{
		if (option_verbose > 2)
			ast_verbose (VERBOSE_PREFIX_3 "sqlitedeltree: Error deleting key from database.\n");
	}

	return 0;
}

static int sqliteput_exec(struct ast_channel *chan, void *data)
{
	int arglen;
	char *argv, *value, *family, *key;

	arglen = strlen (data);
	argv = alloca (arglen + 1);
	if (!argv)			/* Why would this fail? */
	{
		ast_log (LOG_DEBUG, "Memory allocation failed\n");
		return 0;
	}

	memcpy (argv, data, arglen + 1);

	if (strchr (argv, '/') && strchr (argv, '='))
	{
		family = strsep (&argv, "/");
		key = strsep (&argv, "=");
		value = strsep (&argv, "\0");
		if (!value || !family || !key)
		{
			ast_log (LOG_DEBUG, "Ignoring; Syntax error in argument\n");
			return 0;
		}

		if (option_verbose > 2)
			ast_verbose (VERBOSE_PREFIX_3 "sqliteput: family=%s, key=%s, value=%s\n", family, key, value);

		if (ast_db_sqliteput (family, key, value))
		{
			if (option_verbose > 2)
				ast_verbose (VERBOSE_PREFIX_3 "sqliteput: Error writing value to database.\n");
		}

	}
	else
	{
		ast_log (LOG_DEBUG, "Ignoring, no parameters\n");
	}

	return 0;
}

static int sqlitedel_exec(struct ast_channel *chan, void *data)
{
	int arglen;
	char *argv, *family, *key;

	arglen = strlen (data);
	argv = alloca (arglen + 1);
	if (!argv)			/* Why would this fail? */
	{
		ast_log (LOG_DEBUG, "Memory allocation failed\n");
		return 0;
	}

	memcpy (argv, data, arglen + 1);

	if (strchr (argv, '/'))
	{
		family = strsep (&argv, "/");
		key = strsep (&argv, "\0");
		if (!family || !key)
		{
			ast_log (LOG_DEBUG, "Ignoring; Syntax error in argument\n");
			return 0;
		}

		if (option_verbose > 2)
			ast_verbose (VERBOSE_PREFIX_3 "sqlitedel: family=%s, key=%s\n", family, key);

		if (ast_db_sqlitedel (family, key))
		{
			if (option_verbose > 2)
				ast_verbose (VERBOSE_PREFIX_3 "sqlitedel: Error deleting key from database.\n");
		}
	}
	else
	{
		ast_log (LOG_DEBUG, "Ignoring, no parameters\n");
	}

	return 0;
}

static int sqliteget_exec(struct ast_channel *chan, void *data)
{
	int arglen;
	char *argv, *varname, *family, *key;
	char dbresult[256];

	arglen = strlen (data);
	argv = alloca (arglen + 1);
	if (!argv)			/* Why would this fail? */
	{
		ast_log (LOG_DEBUG, "Memory allocation failed\n");
		return 0;
	}

	memcpy (argv, data, arglen + 1);

	if (strchr (argv, '=') && strchr (argv, '/'))
	{
		varname = strsep (&argv, "=");
		family = strsep (&argv, "/");
		key = strsep (&argv, "\0");
		if (!varname || !family || !key)
		{
			ast_log (LOG_DEBUG, "Ignoring; Syntax error in argument\n");
			return 0;
		}

		if (option_verbose > 2)
			ast_verbose (VERBOSE_PREFIX_3 "sqliteget: varname=%s, family=%s, key=%s\n", varname, family, key);

		if (!ast_db_sqliteget (family, key, dbresult, sizeof (dbresult) - 1))
		{
			pbx_builtin_setvar_helper (chan, varname, dbresult);
			if (option_verbose > 2)
				ast_verbose (VERBOSE_PREFIX_3 "sqliteget: set variable %s to %s\n", varname, dbresult);
		}
		else
		{
			if (option_verbose > 2)
				ast_verbose (VERBOSE_PREFIX_3 "sqliteget: Value not found in database.\n");
			  /* Send the call to n+101 priority, where n is the current priority */
			if (ast_exists_extension (chan, chan->context, chan->exten, chan->priority + 101, chan->callerid))
				chan->priority += 100;
		}

	}
	else
	{
		ast_log (LOG_DEBUG, "Ignoring, no parameters\n");
	}

	return 0;
}


static int sqlite_load_module(void)
{
	char *zErr;
	char fn[PATH_MAX];
	int res;

	/* is the database there? */
	snprintf(fn, sizeof(fn), "%s/astdb.db", ast_config_AST_LOG_DIR);
	db = sqlite_open(fn, 0660, &zErr);
	if (!db) {
		ast_log(LOG_ERROR, "app_dbsqlite: %s\n", zErr);
		free(zErr);
		return -1;
	}

	/* is the table there? */
	res = sqlite_exec(db, "SELECT COUNT(Id) FROM astdb;", NULL, NULL, &zErr);
	if (res) {
		res = sqlite_exec(db, sql_create_table, NULL, NULL, &zErr);
		if (res) {
			ast_log(LOG_ERROR, "app_dbsqlite: Unable to create table 'astdb': %s\n", zErr);
			free(zErr);
			goto err;
		}

		/* TODO: here we should probably create an index */
	}
	res = ast_register_application (g_app, sqliteget_exec, g_synopsis, g_descrip);
	if (!res)
		res = ast_register_application (p_app, sqliteput_exec, p_synopsis, p_descrip);
	if (!res)
		res = ast_register_application (d_app, sqlitedel_exec, d_synopsis, d_descrip);
	if (!res)
		res = ast_register_application (dt_app, sqlitedeltree_exec, dt_synopsis, dt_descrip);

	if (res) {
		ast_log(LOG_ERROR, "Unable to register app_dbsqlite\n");
		return -1;
	}
	return 0;

err:
	if (db)
		sqlite_close(db);
	return -1;
}


int sqlite_unload_module(void)
{
	int res;
	if (db)
		sqlite_close(db);
	res = ast_unregister_application (dt_app);
	res |= ast_unregister_application (d_app);
	res |= ast_unregister_application (p_app);
	res |= ast_unregister_application (g_app);
	return res;
}

static int ast_db_sqliteget(char *family, char *key, char *value, int valuelen)
{
	int res = 0;
        char *zErr = 0;
        ast_mutex_lock(&sqlite_lock);
        res=sqlite_exec_printf(db, "SELECT DISTINCT astvalue FROM astdb WHERE astfamily='%q' AND astkey='%q' LIMIT 1", NULL, NULL, &zErr, family, key);
if (res != SQLITE_BUSY && res != SQLITE_LOCKED)
	if (res != SQLITE_BUSY && res != SQLITE_LOCKED)
        	usleep(200);
        if (zErr) {
                ast_log(LOG_ERROR, "sqliteget: %s\n", zErr);
                free(zErr);
        }
        ast_mutex_unlock(&sqlite_lock);
        return res;
}

static int ast_db_sqliteput(char *family, char *key, char *value)
{
	int res = 0;
	char *zErr = 0;
	ast_mutex_lock(&sqlite_lock);
	res=sqlite_exec_printf(db, "DELETE FROM astdb WHERE astfamily='%q' AND astkey='%q'", NULL, NULL, &zErr, family, key);
	if (res != SQLITE_BUSY && res != SQLITE_LOCKED)
		usleep(200);
	if (zErr) {
		ast_log(LOG_ERROR, "sqliteput: %s\n", zErr);
		free(zErr);
	}
	res=sqlite_exec_printf(db, "INSERT INTO astdb (astfamily,astkey,astvalue) VALUES ('%q','%q','%q')", NULL, NULL, &zErr, family, key, value);
	if (res != SQLITE_BUSY && res != SQLITE_LOCKED) {
		usleep(200);
	}
	if (zErr) {
		ast_log(LOG_ERROR, "sqliteput: %s\n", zErr);
		free(zErr);
	}
	ast_mutex_unlock(&sqlite_lock);
	return res;
}

static int ast_db_sqlitedel(char *family, char *key)
{
	int res = 0;
	char *zErr = 0;
	ast_mutex_lock(&sqlite_lock);
	res=sqlite_exec_printf(db, "DELETE FROM astdb WHERE astfamily='%q' AND astkey='%q'", NULL, NULL, &zErr, family, key);
	if (res != SQLITE_BUSY && res != SQLITE_LOCKED) 
		usleep(200);
	if (zErr) {
		ast_log(LOG_ERROR, "sqlitedel: %s\n", zErr);
		free(zErr);
	}
	ast_mutex_unlock(&sqlite_lock);
	return res;
}

static int ast_db_sqlitedeltree(char *family, char *keytree)
{
	int res = 0;
	char *zErr = 0;
	ast_mutex_lock(&sqlite_lock);
	res=sqlite_exec_printf(db, "DELETE FROM astdb WHERE astfamily='%q'", NULL, NULL, &zErr, family);
	if (res != SQLITE_BUSY && res != SQLITE_LOCKED)
		usleep(200);
	if (zErr) {
		ast_log(LOG_ERROR, "sqlitedeltree: %s\n", zErr);
		free(zErr);
	}
	ast_mutex_unlock(&sqlite_lock);
	return res;
}

int unload_module (void)
{
	STANDARD_HANGUP_LOCALUSERS;
	return sqlite_unload_module();
}

int reload(void)
{
	connected = 0;
	sqlite_unload_module();
	return sqlite_load_module();
}

int load_module (void)
{

	return sqlite_load_module();
}

char *description (void)
{
	return tdesc;
}

int usecount (void)
{
	int res;
	STANDARD_USECOUNT (res);
	return res;
}

char *key ()
{
	return ASTERISK_GPL_KEY;
}


