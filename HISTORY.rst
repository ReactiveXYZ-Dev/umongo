=======
History
=======

1.1.0 (2019-01-14)
------------------

* Fix bug when filtering by id in a Document subclass find query (see #145).
* Fix __getattr__ to allow copying and deepcopying Document and EmbeddedDocument
  (see #157).
* Add Document.clone() method (see #158).

1.0.0 (2018-11-29)
------------------
* Raise ``UnknownFieldInDBError`` when an unknown field is found in database
  and not using ``BaseNonStrictDataProxy`` (see #121)
* Fix (non fatal) crash in garbage collector when using ``WrappedCursor`` with
  mongomock
* Depend on pymongo 3.7+ (see #149)
* Pass ``as_marshmallow_schema params`` to nested schemas. Since this change, every
  field's ``as_marshmallow_schema`` method should expect unknown ``**kwargs`` (see #101).
* Pass params to container field in ``ListField.as_marshmallow_schema`` (see #150)
* Add ``meta`` kwarg to ``as_marshmallow_schema`` to pass a ``dict`` of attributes
  for the schema's ``Meta`` class (see #151)

0.15.0 (2017-08-15)
-------------------
* Add `strict` option to (Embedded)DocumentOpts to allow loading of document
  with unknown fields from mongo (see #115)
* Fix fields serialization/deserialization when allow_none is True (see #69)
* Fix ReferenceFild assignment from another ReferenceField (see #110)
* Fix deletion of field proxied by a property (see #109)
* Fix StrictDateTime bonus field: _deserialize does not accept datetime.datetime
  instances (see #106)
* Add force_reload param to Reference.fetch (see #96)

0.14.0 (2017-03-03)
-------------------
* Fix bug in mashmallow tag handling (see #90)
* Fix allow none in DataProxy.set (see #89)
* Support motor 1.1 (see #87)

0.13.0 (2017-01-02)
-------------------

* Fix deserialization error with nested EmbeddedDocuments (see #84, #67)
* Add ``abstract`` and ``allow_inheritance`` options to EmbeddedDocument
* Remove buggy ``as_marshmallow_schema``'s parameter ``missing_accessor`` (see #73, #74)

0.12.0 (2016-11-11)
-------------------

* Replace ``Document.opts.children`` by ``offspring`` and fix grand child
  inheritance issue (see #66)
* Fix dependency since release of motor 1.0 with breaking API

0.11.0 (2016-11-02)
-------------------

* data_objects ``Dict`` and ``List`` inherit builtins ``dict`` and ``list``
* Document&EmbeddedDocument store fields passed during initialization
  as modified (see #50)
* Required field inside embedded document are handled correctly (see #61)
* Document support marshmallow's pre/post processors

0.10.0 (2016-09-29)
-------------------

* Add pre/post update/insert/delete hooks (see #22)
* Provide Umongo to Marshmallow schema/field conversion with
  schema.as_marshmallow_schema() and field.as_marshmallow_field() (see #34)
* List and Dict inherit from collections's UserList and UserDict instead
  of builtins types (needed due to metaprogramming conflict otherwise)
* DeleteError and UpdateError returns the driver result object instead
  of the raw error dict (except for motor which only has raw error dict)

0.9.0 (2016-06-11)
------------------

* Queries can now be expressed with the document's fields name instead of the
  name in database
* ``EmbeddedDocument`` also need to be registered by and instance before use

0.8.1 (2016-05-19)
------------------

* Replace ``Document.created`` by ``is_created`` (see #14)

0.8.0 (2016-05-18)
------------------

* Heavy rewrite of the project, lost of API breakage
* Documents are now first defined as templates then implemented
  inside an Instance
* DALs has been replaced by frameworks implementations of Builder
* Fix ``__getitem__`` for Pymongo.Cursor wrapper
* Add ``conditions`` argument to Document.commit
* Add ``count`` method to txmongo

0.7.8 (2016-4-28)
-----------------

* Fix setup.py style preventing release of version 0.7.7

0.7.7 (2016-4-28)
-----------------

* Fix await error with Reference.fetch
* Pymongo is now only installed with extra flavours of umongo

0.7.6 (2016-4-28)
-----------------

* Use extras_require to install driver along with umongo

0.7.5 (2016-4-23)
-----------------

* Fixing await (Python >= 3.5) support for motor-asyncio

0.7.4 (2016-4-21)
-----------------

* Fix missing package in setup.py

0.7.3 (2016-4-21)
-----------------

* Fix setup.py style preventing from release

0.7.2 (2016-4-21)
-----------------

* Fix crash when generating indexes on EmbeddedDocument

0.7.1 (2016-4-21)
-----------------

* Fix setup.py not to install tests package
* Pass status to Beta

0.7.0 (2016-4-21)
-----------------

* Add i18n support
* Add MongoMock support
* Documentation has been a lot extended

0.6.1 (2016-4-13)
-----------------

* Add ``<dal>_lazy_loader`` to configure Document's lazy_collection

0.6.0 (2016-4-12)
-----------------

* Heavy improvements everywhere !

0.1.0 (2016-1-22)
-----------------

* First release on PyPI.

