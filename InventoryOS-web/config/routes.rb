Rails.application.routes.draw do
  root :to => 'main#index'
  resources :items
  resources :users
  get 'device', :to => 'device#index'
  post 'device/api', :to => 'device#api'
end
