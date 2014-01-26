Dev_Blog2
====

Python Blog System. Powered by Tornado and MongoDB.
[Dev_Blog2](http://scenk.github.io/Dev_Blog2/)

[![Build Status](https://travis-ci.org/ScenK/Dev_Blog2.png?branch=develop)](https://travis-ci.org/ScenK/Dev_Blog2)
[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/ScenK/dev_blog2/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

Features
--------

Dev_Blog2 is Python based CMS system, mainly for bloggers. It can help users to build their blog system easily and quickly.  Also it can be built easily with other web system: 

* Light weight and high performance.

* Theme support.

* Plugin support.

* MondoDB database.

* Easy reading codes and fully in-code docs.

* And much more with continues development…

Get Started
-----------

To get started using Dev_Blog2, clone or fork the master branch or download the released packages. To live the edge, you can also use develop branch. BUT be careful with the crashes :.


Install independences:

    sudo apt-get install python-pip mongodb gcc openjdk-6-jre-headless lessc 

    cd ~/dev_blog2/

    sudo pip install -r requirements.txt

Init website config:

    cp blog/config.py.sample  blog/config.py

    *** change the config with your own config***

    fab build 
  
    *** It will generate a default admin account for you (username/password: admin) ***

Start the website:

    fab test

Much more detail about ***deploy*** in product environment please see ***Docs*** section — ***Build your site***



Browser Support and Testing
---------------------------

Dev_Blog2 is tested and works in:

* IE 7+
* Latest Stable: Firefox, Chrome, Safari
* iOS 6.x, 7.x
* Android 4.x

Much more detail about ***apperence*** please see ***Docs*** section — ***Custom your theme***

Docs and Website
----------------

[My own site](http://tuzii.me) is also open source with an custom theme, and also be include in the ***templates/theme*** folder. 

Contributing
------------

See the  ***Docs*** section — ***Contributing*** for information on how to contribute to Dev_Blog2.


License
-------

This software is free to use under the BSD license.
See the [LICENSE file][] for license text and copyright information.

[LICENSE file]: https://github.com/ScenK/Dev_Blog2/blob/master/LICENSE.md

Dependencies
-------

Thanks to all other open-source projects(may not fully included). 

[Flask](https://github.com/mitsuhiko/flask)
[Mongoengine](https://github.com/MongoEngine/mongoengine)
[Bootstrap-Admin-Template](https://github.com/onokumus/Bootstrap-Admin-Template)


Changelog
-------

