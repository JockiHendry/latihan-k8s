import {PathUtil} from '../app/shared/path-util';

export const environment = {
  production: true,
  backendUrl: PathUtil.generate('https://api.latihan.jocki.me'),
  fileServerUrl: PathUtil.generate('https://files.latihan.jocki.me'),
};
