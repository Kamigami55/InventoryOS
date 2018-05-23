class Item < ApplicationRecord
  belongs_to :holder, class_name: 'User', foreign_key: 'holder_id'
  belongs_to :owner, class_name: 'User', foreign_key: 'owner_id'
end
