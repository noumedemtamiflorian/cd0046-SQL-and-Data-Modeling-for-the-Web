from app import db, Venue, Artist, Show, format_datetime
from datetime import datetime


artist = Artist.query.get(3)

print(artist.past_shows)

# venue1 = Venue.query.get(1)
# venue2 = Venue.query.get(2)
# venue3 = Venue.query.get(3)


# artist1 = Artist.query.get(1)
# artist2 = Artist.query.get(2)
# artist3 = Artist.query.get(3)

# print("\n\n\n")
# print("venue1")
# print("\n")
# print("upcoming_shows : ", venue1.upcoming_shows(), " \n")
# print("\n")
# print("past_shows : ", venue1.past_shows(), " \n")

# print("\n\n\n")
# print("venue2")
# print("\n")
# print("upcoming_shows : ", venue2.upcoming_shows(), " \n")
# print("\n")
# print("past_shows : ", venue2.past_shows(), " \n")

# print("\n\n\n")
# print("venue3")
# print("\n")
# print("upcoming_shows : ", venue3.upcoming_shows(), " \n")
# print("\n")
# print("past_shows : ", venue3.past_shows(), " \n")

# print("\n\n\n")
# print("artist1")
# print("\n")
# print("upcoming_shows : ", artist1.upcoming_shows(), " \n")
# print("\n")
# print("past_shows : ", artist1.past_shows(), " \n")

# print("\n\n\n")
# print("artist2")
# print("\n")
# print("upcoming_shows : ", artist2.upcoming_shows(), " \n")
# print("\n")
# print("past_shows : ", artist2.past_shows(), " \n")

# print("\n\n\n")

# print("artist3")
# print("\n")
# print("upcoming_shows : ", artist3.upcoming_shows(), " \n")
# print("\n")
# print("past_shows : ", artist3.past_shows(), " \n")


# # show2 = Show(start_time=datetime(2022, 12, 5, 5, 6, 5))
# # show3 = Show(start_time=datetime(2021, 12, 5, 5, 6, 5))
# # show4 = Show(start_time=datetime(1999, 12, 5, 5, 6, 5))
# # show5 = Show(start_time=datetime(2024, 12, 5, 5, 6, 5))
# # show6 = Show(start_time=datetime(2025, 12, 5, 5, 6, 5))
# # show7 = Show(start_time=datetime(2026, 12, 5, 5, 6, 5))
# # show8 = Show(start_time=datetime(1998, 12, 5, 5, 6, 5))
# # show9 = Show(start_time=datetime(2000, 12, 5, 5, 6, 5))
# # show10 = Show(start_time=datetime(1995, 12, 5, 5, 6, 5))
# # show11 = Show(start_time=datetime(2012, 12, 5, 5, 6, 5))
# # show12 = Show(start_time=datetime(2045, 12, 5, 5, 6, 5))
# # show13 = Show(start_time=datetime(2015, 12, 5, 5, 6, 5))
# # show14 = Show(start_time=datetime(2012, 12, 5, 5, 6, 5))
# # show15 = Show(start_time=datetime(2019, 12, 5, 5, 6, 5))


# # venue1.shows.append(show3)
# # venue1.shows.append(show4)
# # venue1.shows.append(show6)
# # venue1.shows.append(show7)
# # venue1.shows.append(show8)
# # venue1.shows.append(show13)
# # venue1.shows.append(show15)

# # venue2.shows.append(show3)
# # venue2.shows.append(show4)
# # venue2.shows.append(show6)
# # venue2.shows.append(show7)
# # venue2.shows.append(show8)
# # venue2.shows.append(show14)
# # venue2.shows.append(show15)

# # venue3.shows.append(show2)
# # venue3.shows.append(show3)
# # venue3.shows.append(show4)
# # venue3.shows.append(show6)
# # venue3.shows.append(show8)
# # venue3.shows.append(show9)
# # venue3.shows.append(show14)
# # venue3.shows.append(show15)

# # artist1.shows.append(show2)
# # artist1.shows.append(show3)
# # artist1.shows.append(show5)
# # artist1.shows.append(show6)
# # artist1.shows.append(show11)
# # artist1.shows.append(show12)
# # artist1.shows.append(show14)
# # artist1.shows.append(show15)

# # artist2.shows.append(show2)
# # artist2.shows.append(show3)
# # artist2.shows.append(show5)
# # artist2.shows.append(show6)
# # artist2.shows.append(show7)
# # artist2.shows.append(show11)
# # artist2.shows.append(show13)
# # artist2.shows.append(show14)
# # artist2.shows.append(show15)

# # artist3.shows.append(show2)
# # artist3.shows.append(show3)
# # artist3.shows.append(show4)
# # artist3.shows.append(show5)
# # artist3.shows.append(show8)
# # artist3.shows.append(show9)
# # artist3.shows.append(show12)
# # artist3.shows.append(show14)
# # artist3.shows.append(show15)


# db.session.commit()
