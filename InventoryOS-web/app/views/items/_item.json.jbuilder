json.extract! item, :id, :name, :detail, :status, :location, :owner_id, :holder_id, :category, :main_image_id, :created_at, :updated_at
json.url item_url(item, format: :json)
