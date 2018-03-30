"""
.. module:: aiml
   :synopsis: class objects representing an AIML category tags
   :platform: Any
.. moduleauthor:: Ajeet Singh
"""
from typing import Type, Any
from mysql.connector import MySQLConnection



class Category(object):
    """A category class which represents AIML category tag
    """

    def __init__(self, connection: Type[MySQLConnection], category_id:\
                 int=None, pattern: str=None, template: str=None,\
                 is_system_cmd: bool=False):
        """Default constructor for an category

        Args:
            connection (MySQLConnection): an open connection to mysqldb
            category_id (int): a unique id for an category. if it is valid,\
                    object will be liaded from db
            pattern (str): A pattern for which a template should be returned
            template (str): a template of string form that will be returned if\
                    the pattern matches with user provided text
            is_system_cmd (bool): flag to mark template provided as a system\
            cmd. If true, the template will be executed as sys cmd

        """
        self._connection = connection
        self._category_id = None
        if category_id is not None:
            self._category_id = category_id
        self._pattern = None
        if pattern is not None:
            self._pattern = pattern
        self._prefix = None
        self._suffix = None
        self._ref_that = None
        self._ref_topic = None
        self._is_system_cmd = is_system_cmd
        if is_system_cmd:
            self._system_cmd = template
            self._template = None
        else:
            self._system_cmd = None
            self._template = template
        self._forward_to_category_id = -1
        self._active = False
        self._insert_query = (\
                              'INSERT INTO aiml_categories\
                              (pattern, prefix, suffix, ref_that, ref_topic,\
                              is_system_cmd, system_cmd, template,\
                              forward_to_category_id, active)\
                              VALUES\
                              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'\
                             )
        self._update_query = (\
                              'UPDATE aiml_categories\
                              SET pattern = %s,\
                              prefix = %s,\
                              suffix = %s,\
                              ref_that = %s,\
                              ref_topic = %s,\
                              is_system_cmd = %s,\
                              system_cmd = %s,\
                              template = %s,\
                              forward_to_category_id = %s,\
                              active = %s\
                              WHERE category_id = %s'\
                             )
        self._select_query_by_id = (\
                                    'SELECT\
                                    category_id, pattern, prefix,\
                                    suffix, ref_that, ref_topic, is_system_cmd,\
                                    system_cmd, template, forward_to_category_id, active\
                                    FROM\
                                    aiml_categories\
                                    WHERE\
                                    category_id = %s'\
                                   )
        self._select_query_by_pattern = (\
                                         'SELECT\
                                         category_id, pattern, prefix,\
                                         suffix, ref_that, ref_topic, is_system_cmd, system_cmd, template,\
                                         forward_to_category_id, active\
                                         FROM\
                                         aiml_categories\
                                         WHERE\
                                         pattern = %s'\
                                        )
        self._remove_query = (\
                              'DELETE FROM aiml_categories\
                              WHERE\
                              category_id = %s'\
                             )
        self._load_if_exists_in_db()

    @property
    def category_id(self):
        """
        A unique assigned to an category
        """
        return self._category_id

    @property
    def pattern(self):
        """
        Pattern for current category, this will be matched with user input
        """
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        if value is not None:
            if value != self._pattern:
                self._pattern = value

    @property
    def prefix(self):
        """
        A wildcard (*,^,#,_) or other words to use as prefix for pattern
        """
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        if value != self._prefix:
            self._prefix = value

    @property
    def suffix(self):
        """
        Same as prefix but will be applied as suffix to pattern
        """
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        if value != self._suffix:
            self._suffix = value

    @property
    def ref_that(self):
        """
        AIML that
        """
        return self._ref_that

    @ref_that.setter
    def ref_that(self, value):
        if value != self._ref_that:
            self._ref_that = value

    @property
    def ref_topic(self):
        """
        ref_topic desc
        """
        return self._ref_topic

    @ref_topic.setter
    def ref_topic(self, value):
        if value != self._ref_topic:
            self._ref_topic = value

    @property
    def is_system_cmd(self):
        """
        is_system_cmd desc
        """
        return self._is_system_cmd

    @is_system_cmd.setter
    def is_system_cmd(self, value):
        if value is not None:
            if value != self._is_system_cmd:
                self._is_system_cmd = value

    @property
    def template(self):
        """
        template desc
        """
        return self._template

    @template.setter
    def template(self, value):
        if value != self._template:
            self._template = value

    @property
    def system_cmd(self):
        """
        system_cmd desc
        """
        return self._system_cmd

    @system_cmd.setter
    def system_cmd(self, value):
        if value != self._system_cmd:
            self._system_cmd = value

    @property
    def forward_to_category_id(self):
        """
        forward_to_category_id desc
        """
        return self._forward_to_category_id

    @forward_to_category_id.setter
    def forward_to_category_id(self, value):
        if value != self._forward_to_category_id:
            self._forward_to_category_id = value

    @property
    def active(self):
        """
        active desc
        """
        return self._active

    @active.setter
    def active(self, value):
        if value is not None:
            if value != self._active:
                self._active = value

    def _create(self):
        """Creates a new record in database

        Returns:
            status (bool): true if success else false
        """
        if self._connection is not None:
            _cursor = self._connection.cursor(buffered=True)
            _cursor.execute(self._insert_query, (self.pattern, self.prefix, self.suffix, self.ref_that, self.ref_topic, self.is_system_cmd, self.system_cmd, self.template, self.forward_to_category_id, self.active))
            self._category_id = _cursor.lastrowid
            self._connection.commit()
            return True
        else:
            return False

    def _update(self):
        """Update the db record with the updated values from this object

        Returns:
            status (bool): true if updated successfully else false

        """
        if self._connection is not None and self.category_id is not None:
            _cursor = self._connection.cursor(buffered=True)
            _cursor.execute(self._update_query, (self.pattern, self.prefix, self.suffix, self.ref_that, self.ref_topic, self.is_system_cmd, self.system_cmd, self.template, self.forward_to_category_id, self.active, self.category_id))
            self._connection.commit()
            return True
        else:
            return False

    def _select_by_id(self):
        """select row from db if exists and populate respective fields

        Returns:
            status (bool): return true if record loaded in respective vars else false

        """
        if self._connection is not None and self.category_id is not None:
            _cursor = self._connection.cursor(buffered=True)
            _cursor.execute(self._select_query_by_id, (self.category_id,))
            for (category_id, pattern, prefix, suffix, ref_that, ref_topic, is_system_cmd, system_cmd, template, forward_to_category_id, active) in _cursor:
                self.pattern = pattern
                self.prefix = prefix
                self.suffix = suffix
                self.ref_that = ref_that
                self.ref_topic = ref_topic
                self.is_system_cmd = is_system_cmd
                self.system_cmd = system_cmd
                self.template = template
                self.forward_to_category_id = forward_to_category_id
                self.active = active
            return True
        else:
            return False

    def _select_by_pattern(self):
        """select row from db if exists and populate respective fields

        Returns:
            status (bool): return true if record loaded in respective vars else false

        """
        if self._connection is not None and self.pattern is not None:
            _cursor = self._connection.cursor(buffered=True)
            _cursor.execute(self._select_query_by_pattern, (self.pattern,))
            for (category_id, pattern, prefix, suffix, ref_that, ref_topic, is_system_cmd, system_cmd, template, forward_to_category_id, active) in _cursor:
                self._category_id = category_id
                self.prefix = prefix
                self.suffix = suffix
                self.ref_that = ref_that
                self.ref_topic = ref_topic
                self.is_system_cmd = is_system_cmd
                self.system_cmd = system_cmd
                self.template = template
                self.forward_to_category_id = forward_to_category_id
                self.active = active
            return True
        else:
            return False

    def exists(self):
        """Check record based on category_id or pattern and return true or false accordingly

        Return:
            status (bool): true if record exists in db else false
        """
        if self._connection is not None:
            if self.category_id is not None:
                _query = ('SELECT count(1) as cnt FROM aiml_categories WHERE category_id = %s')
                _cursor = self._connection.cursor(buffered=True)
                _cursor.execute(_query, (self.category_id,))
                for (cnt,) in _cursor:
                    if cnt > 0:
                        return True
                    else:
                        return False
            elif self.pattern is not None:
                _query = ('SELECT count(1) as cnt FROM aiml_categories WHERE pattern = %s')
                _cursor = self._connection.cursor(buffered=True)
                _cursor.execute(_query, (self.pattern,))
                for (cnt,) in _cursor:
                    if cnt > 0:
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False

    def _load_if_exists_in_db(self):
        """Check if record exists in db and loads into object variables
        """
        if self.exists():
            if self.category_id is not None:
                self._select_by_id()
            elif self.pattern is not None:
                self._select_by_pattern()
            else:
                return
        else:
            return

    def save(self):
        """Saves current object by inserting or updating record in db

        Returns:
            status (bool): true if saved else false

        """
        if self._connection is not None:
            if self.exists():
                return self._update()
            else:
                return self._create()
        else:
            return False
