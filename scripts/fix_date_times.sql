-- All earlier datetimes in the database were generated with Django defaults:
-- naive dates and a timezone of 'America/Chicago'. We have changed these
-- settings to use TZ aware dataes and to a timezone of 'America/New_York'.
-- Dkango will now  save the dates as UTC that means that values are off by 6
-- hours for CST dates and 5 hours for CDT dates.
--
-- We can't manipulate these dates via Django as the timestamps are changed
-- automatically throuh Django, so we need to do this in SQL. We can get the
-- Central Time/UTC offset by calculating the difference between the datetime
-- and the datetime converted to UTC
--
-- The test for for whether dates is follows, as shown in this Stackoverflow
-- post:
--
--   http://stackoverflow.com/questions/13879842/mysql-daylight-saving-determine-if-true-or-false
--
-- Thus:
--
--      SELECT CASE
--       WHEN            '2013-07-24 15:00' =
--            CONVERT_TZ('2013-07-24 15:00', 'EST', 'America/New_York')
--       THEN 'no DST' ELSE 'DST' END AS isDST
--
-- Note that I use 'EST'/'America/New_York' below. This is because, I couldn't
-- figure out how to check the difference between 'CST' and 'America/Chicago'
-- local time as there is no 'CST' tz; only 'CST6CDT', and 'CST6CDT' is always
-- equal to 'America/Chicago'. The 'EST' and 'America/New_York' conversion
-- works because during the times differ during DST.
--
-- I suppose, I could try the CST to UTC conversion and see whether the
-- difference is 5 or 6 hours.
--
-- openn_document
-- openn_curatedcollection
-- openn_curatedmembership
-- openn_prepstatus -- updated only
-- openn_version
-- openn_image
-- openn_derivative
--
--  select (time_to_sec(timediff(CONVERT_TZ(created, 'CST6CDT', 'UTC'), created)) / 3600)
--

-- UPDATE openn_document          set created  = convert_tz(created, 'America/Chicago', 'UTC');
-- UPDATE openn_document          set updated  = convert_tz(updated, 'America/Chicago', 'UTC');

-- UPDATE openn_curatedcollection set created  = convert_tz(created, 'America/Chicago', 'UTC');
-- UPDATE openn_curatedcollection set updated  = convert_tz(updated, 'America/Chicago', 'UTC');

-- UPDATE openn_curatedmembership set created  = convert_tz(created, 'America/Chicago', 'UTC');
-- UPDATE openn_curatedmembership set updated  = convert_tz(updated, 'America/Chicago', 'UTC');

-- UPDATE openn_prepstatus        set started  = convert_tz(started, 'America/Chicago', 'UTC');
-- UPDATE openn_prepstatus        set finished = convert_tz(finished, 'America/Chicago', 'UTC');
-- UPDATE openn_prepstatus        set updated  = convert_tz(updated, 'America/Chicago', 'UTC');

-- UPDATE openn_version           set created  = convert_tz(created, 'America/Chicago', 'UTC');
-- UPDATE openn_version           set updated  = convert_tz(updated, 'America/Chicago', 'UTC');

-- UPDATE openn_image             set created  = convert_tz(created, 'America/Chicago', 'UTC');
-- UPDATE openn_image             set updated  = convert_tz(updated, 'America/Chicago', 'UTC');

-- UPDATE openn_derivative        set created  = convert_tz(created, 'America/Chicago', 'UTC');
-- UPDATE openn_derivative        set updated  = convert_tz(updated, 'America/Chicago', 'UTC');


