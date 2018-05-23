class CreateItems < ActiveRecord::Migration[5.2]
  def change
    create_table :items do |t|
      t.string :name
      t.text :detail
      t.string :status
      t.string :location
      t.integer :owner_id
      t.integer :holder_id
      t.string :category
      t.integer :main_image_id

      t.timestamps
    end
  end
end
