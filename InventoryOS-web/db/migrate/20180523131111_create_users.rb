class CreateUsers < ActiveRecord::Migration[5.2]
  def change
    create_table :users do |t|
      t.string :name
      t.string :account
      t.string :password
      t.string :rfid
      t.string :role

      t.timestamps
    end
  end
end
