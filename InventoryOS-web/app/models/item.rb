class Item < ApplicationRecord
  belongs_to :holder, class_name: 'User', foreign_key: 'holder_id', optional: true
  belongs_to :owner, class_name: 'User', foreign_key: 'owner_id'
  mount_uploader :item_image, ItemImageUploader
end
