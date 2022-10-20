0.x.x
=====
* drop python2 support
* add bearer token support

0.2.2
=====
* pingdom returns `verify_certificate` instead of `encryption` for the check-ssl key
  However update api call only accepts `encryption` and will error with `verify_certificate`,
  so we replace `verify_certificate` with `encryption` in the returned check. #78

0.2.1
=====
* Sanitize the data passed to PUT /checks/{check_id} by stripping the
  'verify_certificate' parameter for non-http checks.

0.2.0
=====
* added changelog
* switched legacy, unsupported maintenance window getter to supported rest
  api method

0.3.0
=====
* adjusted API class to work with new Pingdom API 3.1
* introcuded typing to constructors
