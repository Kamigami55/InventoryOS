class User < ApplicationRecord
  has_many :held_items, class_name: 'Item', foreign_key: 'holder_id'
  has_many :owned_items, class_name: 'Item', foreign_key: 'owner_id'
end
