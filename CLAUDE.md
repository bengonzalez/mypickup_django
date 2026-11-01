# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

There is no `requirements.txt`. Installed packages live only in the local venv; per the README, the baseline is:
```
pip install django
pip install pillow
pip install django-crispy-forms
```

Activate the venv first (PowerShell): `.\venv\Scripts\Activate.ps1`. The venv is pinned to Python 3.6.8, which caps dependency versions below what `settings.py`'s docstring suggests (it was generated with Django 4.2.23, but the installed runtime is Django 3.2.25 — Django 4.2 requires Python >=3.8). Don't assume newer package APIs are available without checking what's actually installed.

Common commands (run with the venv's `python`, or activate it first):
- `python manage.py runserver` — start the dev server
- `python manage.py makemigrations [app]` — generate migrations after model changes
- `python manage.py migrate` — apply migrations
- `python manage.py createsuperuser` — create an admin login
- `python manage.py shell` — interactive shell with models loaded
- `python manage.py test` — test runner (no real tests exist yet; `tests.py` in each app is still the generated stub)

Password-reset email sending (`users` app) requires `EMAIL_USER` and `EMAIL_PASS` environment variables (Gmail SMTP, see `mypickup_django/settings.py`).

## Architecture

Three Django apps under one project (`mypickup_django/`):

- **`blog`** — `Post` model (title/content/date_posted) with a `ForeignKey` to `auth.User` as author. Standard class-based views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`). Edit/delete views use `LoginRequiredMixin` + `UserPassesTestMixin`, where `test_func` checks `request.user == post.author` — this is the authorization pattern to follow for any new per-owner editable model.
- **`users`** — registration, login/logout, profile, password reset. `Profile` is a `OneToOneField` to `auth.User`, auto-created and auto-saved via `post_save` signal receivers in `users/signals.py` (wired up in `UsersConfig.ready()`, not imported elsewhere — that's the only place the signal connection happens). `Profile.save()` resizes uploaded images to a 300x300 thumbnail via Pillow.
- **`tns`** — newer app, tracking players/games for a recurring pickup-game group. Models only so far, no views/urls wired up yet. Model chain: `Player` (standalone) → `Venue` (standalone) → `Club` (FK to `Venue`, `on_delete=SET_NULL`) → `Season` (FK to `Club`, `on_delete=CASCADE`) → `Game` (FK to `Season`, `on_delete=CASCADE`; two separate `ForeignKey`s to `Player` for `team1_captain`/`team2_captain`, both `SET_NULL`/nullable; two separate `ManyToManyField`s to `Player` for `team1_players`/`team2_players`). Every FK/M2M that targets `Player` twice on the same model needs a distinct `related_name` to avoid Django's reverse-accessor clash.

Root URLConf (`mypickup_django/urls.py`) wires up admin, all of the `users` auth views (login/logout/register/profile/password reset — note these use `django.contrib.auth.views` directly with custom `template_name`s, not `users/views.py`), and includes `blog.urls` at `/`. `tns` has no URLs included yet. Media files are served through Django itself only when `DEBUG=True`.

## Known gaps

- `Game.team1_captain` / `team2_captain` are not validated to actually be members of `team1_players` / `team2_players`. Django's field types can't express "this FK value must also be in this M2M" — if that invariant needs enforcing, it has to be done in a form's `clean()` or model `clean()`, not the field definitions.
