json.extract! user, :id, :name, :account, :password, :rfid, :role, :created_at, :updated_at
json.url user_url(user, format: :json)
