# Bauteilsortiment

This is a django based webapp which will allow you to manage an electronic components library.

***Warning:** The software currently is in a very early pre-alpha stage. It is very likely that fundamental things will change. You have been warned!*

## Mission statement

This software should allow you to manage a database containing electronic components (resistors, capacitors, ICs, etc.). Various details of these components are stored in the database. The physical components can be stored in assortment boxes and the database should be able to represent that.

Administration of the database entries will happen with the built-in admin interface of django.

Bauteilsortiment will contain generic public views providing lists and detail pages for various data types.

For components, public APIs of common merchants (e.g. digikey) should be used, to automatically fetch details for components (e.g. dimensions, data sheet URLs, etc.) to make the maintenance of the library as easy as possible.

Views should be mobile phone friendly. They should link between the various data-types as they are related in the database.

List views should also be printable, featuring machine readable codes (e.g. qr, data-matrix, etc.) for easy access to details. A common scenario would be that someone points their phone camera at the code to get more details of a component and probably a data-sheet.

## Out of scope

Out of scope for the moment is the creation of edit views and forms. The built in admin pages provided by django will be used instead.

