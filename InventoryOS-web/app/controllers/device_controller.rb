class DeviceController < ApplicationController
  def index
  end
  def image
    @item = Item.last
    image = params[:item_image]
    @item.item_image = image
    @item.save
    render inline: "[UPDATE] Image of (ITEM <%= @item.name %>) updated"
    return
  end
  def api
    #@item_image = api_params[:item_image]
    @username = params[:username]
    @mode = params[:mode]
    @item_name = params[:item_name]

    # Main logic here

    # find user
    @user = User.find_by_name(@username)
    if @user.nil?
      # show error page: user not found TODO
      render inline: "[ABORT] (USER <%= @username %>) not found"
      return
    end

    if @mode == 'BORROW'
      @item = Item.where(name: @item_name, holder_id: nil).first

      if not @item.nil?
        # item in inventory and availiable
        # set item holder to user
        @item.holder = @user
        @item.save
        # show msg TODO
        render inline: "[UPDATE] (USER <%= @user.name %>) successfully BORROW (ITEM <%= @item.name %>)"
        return
      else
        #     //add item to inventory
        #     //set item holder to user
        #     //show edit page(can easily delete)
        # show error msg TODO
        render inline: "[ABORT] Can't find (ITEM <%= @item_name %>) available for borrow"
        return
      end
      # End BORROW

    elsif @mode == 'RETURN'
      @item = @user.held_items.find_by_name(@item_name)
      if not @item.nil?
        # the item the user is holding
        # set no holder for this item
        @item.holder = nil
        @item.save
        # show msg TODO
        render inline: "[UPDATE] (USER <%= @user.name %>) successfully RETURN (ITEM <%= @item.name %>)"
        return
      else
        # show error msg
        render inline: "[ABORT] Can't find (ITEM <%= @item_name %>) that held by (USER <%= @user.name %>)"
        return
      end
      # End RETURN

    elsif @mode == 'ADDNEW'
      # add item to inventory
      @item = Item.new(name: @item_name)
      # set owner to user
      @item.owner = @user
      @item.save
      # show edit page TODO
      render inline: "[UPDATE] ADD new (ITEM <%= @item.name %>) owned by (USER <%= @item.owner.name %>)"
      return
      # End ADDNEW
    end

    render inline: "[ERROR] MODE incorrect or something wrong\n[Raw data] username: <%= @username || 'null' %>, mode: <%= @mode || 'null' %>, item_name: <%= @item_name || 'null' %>"
    return
  end
  # End api

  def item_params
    params.require(:item).permit(:name, :detail, :status, :location, :owner_id, :holder_id, :category, :main_image_id, :item_image)
  end

end
# End class
