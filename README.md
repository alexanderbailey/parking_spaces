# PARKS (Predictive Analysis for Realtime Knowledge of Spaces)


[![Website](https://img.shields.io/badge/site-parks.je-greeb)](https://parks.je)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-red.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

<style>
html {
    height: 100%;
    font-family: "Anta", sans-serif;
    font-weight: 400;
    font-style: normal;
}
.title {
    font-size: 80px;
    color: #eeeeee;
    text-align: center;;
    vertical-align: middle;
    width: 100%;
}

.title img {
    padding-top: 24px;
    height: 80px;
}

.subtitle {
    color: #999999;
    text-align: center;
    width: 100%;
}

.subtitle span {
    color: #eeeeee;
}
</style>
<div class="title">
    PARKS
    <img src="icon.png" />
</div>
<div class="subtitle">
    <span>P</span>redictive
    <span>A</span>nalysis for
    <span>R</span>eal-time
    <span>K</span>nowledge of
    <span>S</span>paces
</div>


---

PARKS is a tool for predicting parking spaces in St. Helier, Jersey.

It's comprised of four components.

## Scraper

It has a script which is scraping the States of Jersey Government website to create a database of parking spaces for each car park. This has been running every minute since the start of 2024.

The Terms and Conditions of the Goverment site require that I reproduce their Copyright statement:

```
Copyright

The material on this site is subject to copyright protection in respect of the States of Jersey unless otherwise indicated.

Copyright protected material may be reproduced free of charge in any format or medium for research, private study or for internal circulation within an organisation. This is subject to the material being reproduced accurately and not being used in a misleading context.

Where any of the copyright items on this site are being republished or copied to others, the source of the material must be identified and the copyright status acknowledged.

The permission to reproduce protected material does not extend to any material on this site for which the copyright is identified as being held by a third party. For authorisation to reproduce such material, you must contact the copyright holder.
```

## API Server

There is a FastAPI server for with a few simple endpoints for uploading and accessing this data.

## Front-end

There is a very basic front-end which plots the spaces for each car park over a 7 day period. This can be accessed from https://parks.je.

## Predictive Model

There is a set of machine learning algorithms created for prediciting the number of spaces at any given time. These will eventually be added to the front-end.


# License

This project is licensed under the GNU General Public License v3.0 (GPLv3).

See [LICENSE](LICENSE) for details.