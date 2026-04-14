def p(x, y):
    # This function saves user data and sends email
    print("Saving data...")
    with open("db.txt", "a") as f:
        f.write(x + "," + y + "\n")
    print("Sending email to " + y)
    # email logic here
    return True

p("John", "john@example.com")
